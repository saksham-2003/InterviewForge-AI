import os
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

Candidate's Answer:
{user_answer}

Evaluate the candidate.

Give:

1. Technical Accuracy (out of 10)

2. Completeness (out of 10)

3. Communication (out of 10)

4. Overall Score (out of 10)

5. Strengths

6. Weaknesses

7. Specific Improvements

Be constructive and detailed.
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

    return response.choices[0].message.content