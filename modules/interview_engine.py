from modules.skill_extractor import extract_skills
from modules.rag_retriever import retrieve_questions
from modules.interview_session import InterviewSession
from modules.answer_evaluator import evaluate_answer


class InterviewEngine:

    def __init__(self):

        self.session = InterviewSession()

    def start_interview(self, resume_text):

        # Extract skills
        skills = extract_skills(resume_text)

        # Convert to query
        if isinstance(skills, str):
            query = skills
        else:
            query = " ".join(skills)

        # Retrieve questions
        questions = retrieve_questions(query)

        # Load questions into session
        self.session.load_questions(questions)

        return self.session

    def get_current_question(self):

        return self.session.get_current_question()

    def submit_answer(self, user_answer):

        current_question = self.session.get_current_question()

        evaluation = evaluate_answer(
            current_question["question"],
            current_question["answer"],
            user_answer
        )

        self.session.save_answer(user_answer)

        self.session.save_evaluation(evaluation)

        return evaluation

    def next_question(self):

        self.session.next_question()

        return self.session.get_current_question()