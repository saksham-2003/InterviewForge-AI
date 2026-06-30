import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def evaluate_answer(question, ideal_answer, user_answer):

    prompt = f"""
You are a senior technical interviewer.

Question:
{question}

Ideal Answer:
{ideal_answer}

Candidate Answer:
{user_answer}

Evaluate the answer and return ONLY a valid JSON object.

Format:

{{
    "technical_accuracy": 0,
    "completeness": 0,
    "communication": 0,
    "overall_score": 0,
    "strengths": [
        "...",
        "..."
    ],
    "weaknesses": [
        "...",
        "..."
    ],
    "improvements": [
        "...",
        "...",
        "..."
    ],
    "summary": "Short overall feedback"
}}

Rules:

- Scores must be between 0 and 10.
- Return ONLY JSON.
- No markdown.
- No explanation outside JSON.
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

    result = json.loads(
        response.choices[0].message.content
    )   

    result["overall_score"] = float(
        result["overall_score"]
    )

    return result