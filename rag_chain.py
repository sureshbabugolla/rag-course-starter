# rag_chain.py
# RAG Course — Exercise 3: Full RAG Pipeline
#
# GOAL: Connect retriever → prompt template → Ollama LLM → grounded answer
#
# Run ingest.py first before running this file!
# ─────────────────────────────────────────────────────────────────────────────

import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Silence ChromaDB telemetry warnings
os.environ["ANONYMIZED_TELEMETRY"] = "false"

# ── Configuration ─────────────────────────────────────────────────────────────
CHROMA_DB_PATH  = os.getenv("CHROMA_DB_PATH", "./chroma_db")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL       = "mistral:7b-instruct"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ── Prompt Template ───────────────────────────────────────────────────────────
# TODO: Fill in the prompt template below
# It should instruct the LLM to:
#   1. Answer using ONLY the provided context
#   2. Say "I don't have enough information" if the answer isn't in the context
#   3. Use {context} and {question} as placeholders

RAG_PROMPT_TEMPLATE = """
TODO: Write your prompt template here.
Remember to include {context} and {question} placeholders.
"""


def format_docs(docs: list) -> str:
    # TODO: Join all retrieved document chunks into one string
    # Hint: "\n\n".join(doc.page_content for doc in docs)
    pass


def build_rag_chain():

    # ── Step 1: Load vector store and create retriever ────────────────────────
    # Hint: vectorstore.as_retriever(search_kwargs={"k": 3})
    # TODO: Load embedding model, load ChromaDB, create retriever



    # ── Step 2: Load the local LLM via Ollama ─────────────────────────────────
    # Hint: OllamaLLM(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
    # TODO: Write your code here



    # ── Step 3: Build the prompt ──────────────────────────────────────────────
    # Hint: PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    # TODO: Write your code here



    # ── Step 4: Build the LCEL chain ──────────────────────────────────────────
    # Flow: {context: retrieve+format, question: passthrough} | prompt | llm | parse
    # Hint: chain = ({"context": retriever | format_docs, "question": RunnablePassthrough()}
    #               | prompt | llm | StrOutputParser())
    # TODO: Write your code here



    return chain


def ask(chain, question: str) -> str:
    print(f"\n{'='*60}")
    print(f"❓ Question: {question}")
    print(f"{'='*60}")
    print("⏳ Retrieving and generating answer...")

    # TODO: Call chain.invoke(question) and store the result
    answer = None  # replace this

    print(f"\n💬 Answer:\n{answer}")
    return answer


if __name__ == "__main__":
    print("🚀 Initializing RAG chain...")
    chain = build_rag_chain()
    print("✅ RAG chain ready!\n")

    ask(chain, "What is the return policy?")
    ask(chain, "How do I contact customer support?")
    ask(chain, "What is the capital of France?")   # Out of scope!
