# retriever.py
# RAG Course — Exercise 2: Query the Vector Store
#
# GOAL: Load ChromaDB → run a similarity search → inspect retrieved chunks
#
# Run ingest.py first before running this file!
# ─────────────────────────────────────────────────────────────────────────────

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ── Configuration ─────────────────────────────────────────────────────────────
CHROMA_DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def search(query: str, k: int = 3):

    # ── Step 1: Load the embedding model ──────────────────────────────────────
    # Use the SAME model as ingestion — must match or results will be wrong!
    # Hint: HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    # TODO: Write your code here



    # ── Step 2: Load the existing ChromaDB vector store ───────────────────────
    # Hint: Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embedding)
    # TODO: Write your code here



    # ── Step 3: Run a similarity search ───────────────────────────────────────
    # Returns the k most similar chunks to the query
    # Hint: vectorstore.similarity_search_with_score(query, k=k)
    # TODO: Write your code here



    return results


if __name__ == "__main__":

    # ── Test with different queries ────────────────────────────────────────────
    # Try changing these queries and observe how the retrieved chunks change!
    test_queries = [
        "What is the return policy?",
        "How do I contact customer support?",
        "What products does ACME sell?",
        "What is the weather forecast?",   # Not in knowledge base — what happens?
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"🔍 Query: {query}")
        print(f"{'='*60}")

        results = search(query, k=3)

        for i, (doc, score) in enumerate(results):
            print(f"\n📄 Chunk {i+1} | Similarity Score: {score:.4f}")
            print(f"Content: {doc.page_content[:200]}...")

        # ── EXPERIMENT: notice the score for the out-of-scope query ───────────
        # A low similarity score = the vector DB has no good match
        # This is why we tell the LLM to say "I don't know" when context is weak
