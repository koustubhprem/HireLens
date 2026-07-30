from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
from dotenv import load_dotenv

try:
    from ResumeBuilder.ai_responses import ai_score_fit
    from ResumeBuilder.text_extractor import parse_resume
except ImportError:
    from ai_responses import ai_score_fit
    from text_extractor import parse_resume

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI(title="AI Job Fit Analyzer")

# Jinja2 templates and static files
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
):
    # 1. Parse resume
    resume_text, resume_text_length, resume_preview = await parse_resume(resume_file)
    jd_length = len(job_description.strip())

    # 2. Call AI scoring function (Gemini or Groq)
    fit_data = await ai_score_fit(
        resume_text=resume_text,
        jd_text=job_description,
    )

    overall_fit = fit_data.get("overall_fit", 0)
    experience_fit = fit_data.get("experience_fit", 0)
    technical_fit = fit_data.get("technical_fit", 0)
    strengths = fit_data.get("strengths", [])
    gaps = fit_data.get("gaps", [])

    # 3. Render template with AI scores + explanations
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "resume_filename": resume_file.filename,
            "resume_text_length": resume_text_length,
            "resume_preview": resume_preview,
            "job_description": job_description,
            "jd_length": jd_length,
            "overall_fit": overall_fit,
            "experience_fit": experience_fit,
            "technical_fit": technical_fit,
            "strengths": strengths,
            "gaps": gaps,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)