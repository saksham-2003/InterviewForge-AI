from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_resume(resume_text):

    prompt = f"""
    You are an AI Resume Analyzer.

    Extract the following information from the resume:

    1. Full Name
    2. Skills
    3. Projects
    4. Experience
    5. Education

    Resume:
    {resume_text}

    Return the information in a clean and structured format.
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

    return response.choices[0].message.content