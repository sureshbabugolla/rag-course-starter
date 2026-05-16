# solutions/rag_chain.py
# COMPLETE SOLUTION — only peek if you're stuck!
# ─────────────────────────────────────────────────────────────────────────────

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

CHROMA_DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "mistral:7b-instruct"

RAG_PROMPT_TEMPLATE = """You are a helpful and precise assistant.
Answer the user's question using ONLY the information provided in the context below.
If the answer cannot be found in the context, respond with:
"I don't have enough information to answer that based on the available documents."
Do not make up information or use your general knowledge.

Context:
{context}

Question: {question}

Answer:"""


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain():
    # Step 1: Load vector store and retriever
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding,
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Step 2: Load LLM
    llm = OllamaLLM(model=LLM_MODEL, temperature=0)

    # Step 3: Build prompt
    prompt = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

    # Step 4: Build LCEL chain
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def ask(chain, question: str) -> str:
    print(f"\n{'='*60}")
    print(f"❓ Question: {question}")
    print(f"{'='*60}")
    print("⏳ Retrieving and generating answer...")
    answer = chain.invoke(question)
    print(f"\n💬 Answer:\n{answer}")
    return answer


if __name__ == "__main__":
    print("🚀 Initializing RAG chain...")
    chain = build_rag_chain()
    print("✅ RAG chain ready!\n")

    ask(chain, "What is the return policy?")
    ask(chain, "How do I contact customer support?")
    ask(chain, "What is the capital of France?")
