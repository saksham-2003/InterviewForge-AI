import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_questions(skills, retrieved_context):
    prompt = f"""
    The candidate has these skills:

    {skills}

    The following questions were retrieved from our interview knowledge base:

    {retrieved_context}

    Using these retrieved questions as context,
    generate:

    5 Easy interview questions
    5 Medium interview questions
    5 Hard interview questions.

    The questions should be:
    1. Personalized to the candidate's skills.
    2. More advanced than the retrieved questions.
    3. Similar to real interview questions.

    Format the response nicely.
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