
import os
from dotenv import load_dotenv
from groq import Groq
import ast

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_skills(resume_text):

    prompt = f"""
    Extract ONLY the technical skills from this resume.

    Return ONLY a valid Python list.

    Example:
    ["Python", "Machine Learning", "ReactJS"]

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    skills = response.choices[0].message.content

    return skills