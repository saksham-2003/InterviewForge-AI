class InterviewSession:

    def __init__(self):

        self.questions = []

        self.current_question = 0

        self.answers = []

        self.evaluations = []

        self.total_score = 0

        self.completed = False

    def load_questions(self, questions):
        self.questions = questions

    def get_current_question(self):

        if self.current_question < len(self.questions):
            return self.questions[self.current_question]

        return None

    def save_answer(self, answer):
        self.answers.append(answer)

    def save_evaluation(self, evaluation):
        self.evaluations.append(evaluation)

    def add_score(self, score):
        self.total_score += score

    def next_question(self):
        self.current_question += 1

        if self.current_question >= len(self.questions):
            self.completed = True

    def interview_finished(self):
        return self.completed

    def average_score(self):

        if len(self.evaluations) == 0:
            return 0

        return round(
            self.total_score / len(self.evaluations),
            2
        )
    def get_report(self):

        return {
            "questions_answered": len(self.answers),
            "total_questions": len(self.questions),
            "average_score": self.average_score(),
            "evaluations": self.evaluations
        }