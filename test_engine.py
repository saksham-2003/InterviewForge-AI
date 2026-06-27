from modules.interview_engine import InterviewEngine

resume = """

Python
Machine Learning
Deep Learning
PyTorch
Computer Vision
YOLO
OpenCV

"""

engine = InterviewEngine()

session = engine.start_interview(
    resume
)

print("\nInterview Started\n")

print(session.get_current_question())