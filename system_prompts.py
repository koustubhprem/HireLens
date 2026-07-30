FIT_SCORING_SYSTEM = """
You are an expert hiring manager and career coach.
Given a resume and a job description, you will:
- Rate the candidate's fit numerically.
- Explain strengths and gaps.
Return your answer as strict JSON that matches the schema.
"""

FIT_SCORING_USER_TEMPLATE = """
Job description:
---
{jd_text}
---

Candidate resume:
---
{resume_text}
---

Task:
Return a JSON object with this exact structure:

{{
  "overall_fit": <number 0-100>,
  "experience_fit": <number 0-100>,
  "technical_fit": <number 0-100>,
  "strengths": [<string>, ...],
  "gaps": [<string>, ...]
}}

Constraints:
- Use only integers or one decimal place for scores.
- strengths and gaps must be concise bullet points, not paragraphs.
"""