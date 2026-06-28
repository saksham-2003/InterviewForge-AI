from modules.skill_extractor import extract_skills
from modules.rag_retriever import retrieve_questions
from modules.interview_session import InterviewSession
from modules.answer_evaluator import evaluate_answer


class InterviewEngine:

    def __init__(self):

        self.session = InterviewSession()

    def start_interview(
    self,
    resume_text,
    level="Graduate"
    ):

        # Extract skills
        skills = extract_skills(resume_text)

        # Convert to query
        if isinstance(skills, str):
            query = skills
        else:
            query = " ".join(skills)

         # Decide interview difficulty distribution

        if level == "Graduate":

            easy_count = 7
            medium_count = 3
            hard_count = 0

        elif level == "Professional":

            easy_count = 2
            medium_count = 6
            hard_count = 2

        else:   # Expert

            easy_count = 0
            medium_count = 3
            hard_count = 7

        # Retrieve questions
        all_questions = retrieve_questions(query, k=20)

        easy_questions = []
        medium_questions = []
        hard_questions = []

        for question in all_questions:

            difficulty = question["difficulty"].strip().lower()

            if difficulty == "easy":
                easy_questions.append(question)

            elif difficulty == "medium":
                medium_questions.append(question)

            elif difficulty == "hard":
                hard_questions.append(question)

        
        questions = []

        questions.extend(easy_questions[:easy_count])
        questions.extend(medium_questions[:medium_count])
        questions.extend(hard_questions[:hard_count])

        remaining = 10 - len(questions)

        if remaining > 0:

            extra_questions = (
                easy_questions[easy_count:] +
                medium_questions[medium_count:] +
                hard_questions[hard_count:]
            )

            questions.extend(extra_questions[:remaining])
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

        if self.session.interview_finished():
            return None

        return self.session.get_current_question()