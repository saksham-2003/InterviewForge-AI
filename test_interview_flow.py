from modules.interview_session import InterviewSession
from modules.rag_retriever import retrieve_questions

session = InterviewSession()

questions = retrieve_questions(
    "PyTorch Computer Vision"
)

session.load_questions(questions)

current = session.get_current_question()

print("\nCurrent Question:\n")

print(current)