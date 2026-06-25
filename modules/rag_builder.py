from sentence_transformers import SentenceTransformer
import faiss
import pickle

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Reading questions...")

with open(
    "data/interview_questions.txt",
    "r",
    encoding="utf-8"
) as file:
    questions = file.readlines()

questions = [q.strip() for q in questions]

print(f"Loaded {len(questions)} questions")

print("Creating embeddings...")

embeddings = model.encode(
    questions,
    convert_to_numpy=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(
    index,
    "vector_store/interview.index"
)

with open(
    "vector_store/questions.pkl",
    "wb"
) as f:
    pickle.dump(
        questions,
        f
    )

print("Vector database created successfully!")