from groq import Groq
from dotenv import load_dotenv
from modules.ats_score_calculator import ATSScoreCalculator
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def check_ats(resume_text):
    calculator = ATSScoreCalculator(
        resume_text
    )

    rule_scores = calculator.calculate()

    prompt = f"""
You are an expert ATS Resume Coach.

A rule-based ATS engine has already analyzed this resume.

Resume:

{resume_text}

Rule-Based ATS Results:

{rule_scores}

Your job is NOT to calculate scores.

Instead, explain the results.

Return ONLY JSON.

{{
    "strengths":[
        "...",
        "..."
    ],
    "missing_skills":[
        "...",
        "..."
    ],
    "suggestions":[
        "...",
        "...",
        "..."
    ],
    "summary":"..."
}}

Rules:

- Do NOT generate scores.
- Do NOT change the calculated scores.
- Explain the resume.
- Return ONLY valid JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    result = response.choices[0].message.content

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    print(result)

    result = json.loads(result)

    result["rule_based_scores"] = rule_scores

    return result