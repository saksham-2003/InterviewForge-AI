from modules.interview_session import InterviewSession

session = InterviewSession()

session.load_questions([
    "What is Python?",
    "Explain Transfer Learning."
])

print(session.get_current_question())

session.save_answer(
    "Python is a programming language."
)

session.save_evaluation(
    "Score: 8/10"
)

session.next_question()

print(session.get_current_question())