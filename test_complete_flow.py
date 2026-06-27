from modules.interview_engine import InterviewEngine

resume = """
Python
Machine Learning
PyTorch
YOLO
OpenCV
"""

engine = InterviewEngine()

engine.start_interview(resume)

question = engine.get_current_question()

print("\nQuestion:\n")

print(question["question"])

print("\nSubmitting answer...\n")

evaluation = engine.submit_answer(

    "YOLO detects objects in one stage while Faster R-CNN uses region proposals."

)

print(evaluation)

print("\nNext Question:\n")

next_question = engine.next_question()

print(next_question["question"])