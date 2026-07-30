# HireLens — AI Job Fit Analyzer

An AI-powered tool that analyzes how well a resume matches a job description, using LLMs (Gemini and Groq) to score fit, highlight strengths and gaps, and (in progress) generate tailored resumes and cover letters.

## Status: v0.1.0 (MVP)

This is an early-stage MVP built as a portfolio project to demonstrate practical GenAI engineering and data science skills: prompt design, structured LLM outputs, multi-provider orchestration, and full-stack Python development.

## Features (current)

- Upload a resume (PDF) and paste a job description
- Automatic resume text extraction and parsing
- AI-generated fit analysis via Gemini or Groq LLMs, returning:
  - Overall fit score
  - Experience fit score
  - Technical fit score
  - Key strengths
  - Key gaps / areas to improve
- Simple FastAPI + Jinja2 web interface

## Features (roadmap)

- [ ] **LLM Council scoring** — multiple LLMs independently score the resume/JD fit, then a "chair" model synthesizes a final consensus rating (inspired by mixture-of-experts and LLM-as-judge patterns)
- [ ] Company research — pull context on the company and role requirements
- [ ] Salary/compensation suggestions based on role, seniority, and location
- [ ] Discovery of other open roles at the same company matching the candidate's skillset
- [ ] AI-tailored resume rewriting with downloadable PDF export
- [ ] AI-generated cover letter tailored to the role and company

## Tech Stack

- **Backend:** Python, FastAPI
- **Templating:** Jinja2 (HTML/CSS)
- **AI/LLM providers:** Google Gemini (Interactions API), Groq (Llama models)
- **Resume parsing:** PyPDF2 / pdfminer
- **Environment management:** python-dotenv

## Project Structure

\`\`\`text
ResumeBuilder/
├── app.py                 # FastAPI app and routes
├── ai_responses.py        # LLM calls, prompt building, response parsing
├── system_prompts.py      # System and user prompt templates
├── text_extractor.py      # Resume (PDF) parsing utilities
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   └── result.html
├── static/                 # Static assets
├── css/
│   └── style.css
├── .env.example            # Template for required environment variables
├── .gitignore
└── README.md
\`\`\`

## Setup

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/koustubhprem/ResumeBuilder.git
   cd ResumeBuilder
   \`\`\`

2. Create and activate a virtual environment:
   \`\`\`bash
   python -m venv .venv
   .venv\\Scripts\\activate   # Windows
   source .venv/bin/activate  # macOS/Linux
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Set up environment variables:
   - Copy \`.env.example\` to \`.env\`
   - Add your API keys:
     \`\`\`env
     GEMINI_API_KEY=your_gemini_key_here
     GROQ_API_KEY=your_groq_key_here
     LLM_PROVIDER=gemini
     \`\`\`

5. Run the app:
   \`\`\`bash
   uvicorn app:app --reload
   \`\`\`

6. Open \`http://localhost:8000\` in your browser.

## Why this project

This project was built to demonstrate practical, end-to-end GenAI engineering skills relevant to Data Scientist / GenAI Engineer roles:

- Designing structured prompts that return reliable, parseable JSON from LLMs
- Orchestrating multiple LLM providers (Gemini, Groq) behind a single interface
- Building a full-stack Python application (FastAPI backend + templated frontend)
- Iterating toward a multi-agent "LLM council" evaluation pattern for more robust, less biased scoring

How does the output look like:
<img width="959" height="413" alt="image" src="https://github.com/user-attachments/assets/1377b5ee-8a5f-4771-a7f8-9fa4a9575428" />
<img width="951" height="437" alt="image" src="https://github.com/user-attachments/assets/9c64f8d7-898e-4fa0-bbfd-e00a0b37991f" />



## License

MIT (or update as preferred)
