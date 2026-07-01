import pickle

# ---------------------------------------------------------------------------
# Module-level sentinels — nothing is loaded at import time.
# All three resources are initialised lazily on the first call to
# retrieve_questions(), so importing this module never triggers a network
# request, a disk read, or a crash due to missing vector-store files.
# ---------------------------------------------------------------------------

_model = None
_index = None
_questions = None


def _ensure_loaded():
    """Load the embedding model, FAISS index, and question DataFrame exactly
    once, on demand. Subsequent calls return immediately because all three
    sentinels are already populated after the first call."""

    global _model, _index, _questions

    if _model is None:
        from sentence_transformers import SentenceTransformer
        import faiss

        _model = SentenceTransformer("all-MiniLM-L6-v2")

    try:
        if _index is None:
            _index = faiss.read_index("vector_store/interview.index")

        if _questions is None:
            with open("vector_store/questions.pkl", "rb") as f:
                _questions = pickle.load(f)

    except FileNotFoundError:
        raise RuntimeError(
            "Vector store not found. Please run rag_builder.py first."
        )


def retrieve_questions(query, k=5):

    _ensure_loaded()

    query_embedding = _model.encode(
        [query]
    )

    distances, indices = _index.search(
        query_embedding,
        k
    )

    results = []

    for idx in indices[0]:

        row = _questions.iloc[idx]

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