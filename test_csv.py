import pandas as pd

df = pd.read_csv(
    "data/interview_questions.csv"
)

print(df.head())
print("\nRows:", len(df))
print("\nColumns:")
print(df.columns)