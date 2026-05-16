# app.py
# RAG Course — Exercise 4 (Bonus): Interactive CLI App
#
# GOAL: Wrap rag_chain.py in an interactive loop so users can
#       keep asking questions without restarting the script.
#
# Run ingest.py first before running this file!
# ─────────────────────────────────────────────────────────────────────────────

from rag_chain import build_rag_chain, ask


def main():
    print("\n" + "="*60)
    print("  🤖 RAG Assistant — Powered by LangChain + Ollama")
    print("  Knowledge Base: ACME Corporation Support Docs")
    print("="*60)
    print("Type your question and press Enter.")
    print("Type 'quit' to exit.\n")

    # ── Step 1: Build the RAG chain (loads models + vector store) ─────────────
    # Hint: chain = build_rag_chain()
    # TODO: Write your code here



    print("✅ Assistant ready! Ask me anything about ACME products.\n")

    # ── Step 2: Interactive loop ───────────────────────────────────────────────
    # Keep asking for input until the user types 'quit' or 'exit'
    # Hint: use a while True loop with input() to get the user's question
    # TODO: Write your loop here
    # Remember to:
    #   - Strip whitespace from input
    #   - Skip empty input
    #   - Break on 'quit', 'exit', or 'q'
    #   - Call ask(chain, question) for valid questions



if __name__ == "__main__":
    main()
