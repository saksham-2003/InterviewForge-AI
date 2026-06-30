from modules.ats_score_calculator import ATSScoreCalculator

resume = """

Saksham Lakhani

saksham@gmail.com

+91 9876543210

LinkedIn

GitHub

B.Tech Information Technology

CGPA 8.05

"""

calculator = ATSScoreCalculator(resume)

print(calculator.calculate())