from sentence_transformers import SentenceTransformer
import faiss
import pickle

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "vector_store/interview.index"
)

with open(
    "vector_store/questions.pkl",
    "rb"
) as f:
    questions = pickle.load(f)


def retrieve_questions(query, k=5):

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for idx in indices[0]:

        row = questions.iloc[idx]

        results.append(
            {
                "question": row["question"],
                "category": row["category"],
                "difficulty": row["difficulty"],
                "company": row["company"],
                "role": row["role"],
                "answer": row["answer"]
            }
        )

    return results