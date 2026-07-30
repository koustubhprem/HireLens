import os
from dotenv import load_dotenv
load_dotenv()

from google import genai         # Gemini Interactions API client
from groq import Groq            # Groq Python client

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

import json
from typing import Dict

try:
    from ResumeBuilder.system_prompts import FIT_SCORING_SYSTEM, FIT_SCORING_USER_TEMPLATE
except ImportError:
    from system_prompts import FIT_SCORING_SYSTEM, FIT_SCORING_USER_TEMPLATE


def _build_fit_scoring_prompt(resume_text: str, jd_text: str) -> str:
    return FIT_SCORING_USER_TEMPLATE.format(
        jd_text=jd_text,
        resume_text=resume_text,
    )


async def ai_score_fit(resume_text: str, jd_text: str) -> Dict:
    """
    Use Gemini or Groq to produce structured fit scores and explanations.

    Returns a dict with keys:
    - overall_fit
    - experience_fit
    - technical_fit
    - strengths
    - gaps
    """
    prompt = _build_fit_scoring_prompt(resume_text, jd_text)

    raw_output = ""

    # Gemini path
    if LLM_PROVIDER == "gemini" and gemini_client is not None:
        interaction = gemini_client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt,
            system_instruction=FIT_SCORING_SYSTEM,
        )
        raw_output = interaction.output_text

    # Groq path
    elif LLM_PROVIDER == "groq" and groq_client is not None:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": FIT_SCORING_SYSTEM},
                {"role": "user", "content": prompt},
            ],
        )
        raw_output = completion.choices[0].message.content

    else:
        # Fallback if no API keys
        return {
            "overall_fit": 0,
            "experience_fit": 0,
            "technical_fit": 0,
            "strengths": ["LLM provider is not configured."],
            "gaps": [],
        }

    # Strip code fences (```json ... ```) if present
    cleaned = raw_output.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.split("\n", 1)[-1]

    # Parse JSON
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "overall_fit": 0,
            "experience_fit": 0,
            "technical_fit": 0,
            "strengths": ["Could not parse AI output as JSON."],
            "gaps": [],
        }

    return data