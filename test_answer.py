from modules.answer_evaluator import evaluate_answer

question = "What is Transfer Learning?"

ideal = """
Transfer learning is the process of taking a model pretrained on one task
and fine tuning it on another related task.
"""

user = """
It means using an already trained model for another problem.
"""

result = evaluate_answer(
    question,
    ideal,
    user
)

print(result)