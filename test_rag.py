from modules.rag_retriever import retrieve_questions

results = retrieve_questions(
    "PyTorch YOLO Computer Vision"
)

for i, question in enumerate(results, 1):

    print(f"\nQuestion {i}")
    print(question)