import pandas as pd
import os

folder = "data"

files = [
    "batch1.csv",
    "batch2.csv",
    "batch3.csv",
    "batch4.csv",
    "batch5.csv"
]

dfs = []

for file in files:
    path = os.path.join(folder, file)

    df = pd.read_csv(path)

    dfs.append(df)

merged_df = pd.concat(
    dfs,
    ignore_index=True
)

# Remove duplicates if any
merged_df = merged_df.drop_duplicates(
    subset=["question"]
)

merged_df.to_csv(
    "data/interview_dataset.csv",
    index=False
)

print(
    f"Dataset created successfully!"
)

print(
    f"Total Questions: {len(merged_df)}"
)