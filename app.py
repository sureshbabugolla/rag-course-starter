# solutions/app.py — COMPLETE SOLUTION
from rag_chain import build_rag_chain, ask


def main():
    print("\n" + "="*60)
    print("  🤖 RAG Assistant — Powered by LangChain + Ollama")
    print("  Knowledge Base: ACME Corporation Support Docs")
    print("="*60)
    print("Type your question and press Enter.")
    print("Type 'quit' to exit.\n")

    chain = build_rag_chain()
    print("✅ Assistant ready! Ask me anything about ACME products.\n")

    while True:
        try:
            question = input("You: ").strip()
            if not question:
                continue
            if question.lower() in ("quit", "exit", "q", "bye"):
                print("\n👋 Goodbye!")
                break
            ask(chain, question)
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
