# solutions/retriever.py — COMPLETE SOLUTION
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

os.environ["ANONYMIZED_TELEMETRY"] = "false"

CHROMA_DB_PATH  = "./chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def search(query: str, k: int = 3):
    # Step 1: Load embedding model
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Step 2: Load ChromaDB
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding,
    )

    # Step 3: Similarity search
    results = vectorstore.similarity_search_with_score(query, k=k)
    return results


if __name__ == "__main__":
    test_queries = [
        "What is the return policy?",
        "How do I contact customer support?",
        "What products does ACME sell?",
        "What is the weather forecast?",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"🔍 Query: {query}")
        print(f"{'='*60}")
        results = search(query, k=3)
        for i, (doc, score) in enumerate(results):
            print(f"\n📄 Chunk {i+1} | Similarity Score: {score:.4f}")
            print(f"Content: {doc.page_content[:200]}...")
