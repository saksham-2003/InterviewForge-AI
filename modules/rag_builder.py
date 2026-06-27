import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import pickle

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Reading CSV dataset...")

df = pd.read_csv(
    "data/interview_dataset.csv"
)

df["answer"] = df["answer"].fillna(
    "Answer not available."
)

questions = df["question"].tolist()

print(f"Loaded {len(questions)} questions")

print("Creating embeddings...")

embeddings = model.encode(
    questions,
    convert_to_numpy=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    embeddings
)

faiss.write_index(
    index,
    "vector_store/interview.index"
)

with open(
    "vector_store/questions.pkl",
    "wb"
) as f:
    pickle.dump(
        df,
        f
    )

print("Vector database created successfully!")