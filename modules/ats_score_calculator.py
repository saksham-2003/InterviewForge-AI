import re


class ATSScoreCalculator:

    def __init__(self, resume_text):

        self.resume = resume_text.lower()

    def calculate(self):

        report = {
            "contact_score": self.contact_score(),
            "education_score": self.education_score(),
            "skills_score": self.skills_score(),
            "projects_score": self.projects_score(),
            "experience_score": self.experience_score()
        }

        report["overall_score"] = round(
            (
                report["contact_score"] +
                report["education_score"] +
                report["skills_score"] +
                report["projects_score"] +
                report["experience_score"]
            ) / 5
        )

        return report

    def contact_score(self):

        score = 0

        if re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            self.resume
        ):
            score += 25

        if re.search(
            r"\+?\d[\d\s-]{8,}",
            self.resume
        ):
            score += 25

        if "linkedin" in self.resume:
            score += 25

        if "github" in self.resume:
            score += 25

        return score

    def education_score(self):

        keywords = [
            "b.tech",
            "btech",
            "bachelor",
            "master",
            "cgpa",
            "university",
            "college"
        ]

        score = 0

        for word in keywords:

            if word in self.resume:
                score += 15

        return min(score, 100)

    def skills_score(self):

        skills = [
            "python",
            "java",
            "c++",
            "javascript",
            "sql",
            "react",
            "node",
            "tensorflow",
            "pytorch",
            "machine learning",
            "deep learning",
            "opencv",
            "git",
            "docker",
            "aws"
        ]

        found = 0

        for skill in skills:

            if skill in self.resume:
                found += 1

        return round((found / len(skills)) * 100)

    def projects_score(self):

        project_keywords = [
            "project",
            "developed",
            "implemented",
            "built",
            "designed",
            "created"
        ]

        score = 0

        for word in project_keywords:

            if word in self.resume:
                score += 20

        return min(score, 100)

    def experience_score(self):

        experience_keywords = [
            "intern",
            "internship",
            "experience",
            "worked",
            "software engineer",
            "developer",
            "research"
        ]

        score = 0

        for word in experience_keywords:

            if word in self.resume:
                score += 15

        return min(score, 100)