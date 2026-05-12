"""
Minimal RAG chatbot scaffold.

This file deliberately leaves the language-model call as a placeholder.
Students must connect it to their chosen local model or approved hosted API.

The starter implementation prints the RAG prompt so that the retrieval and
prompt construction pipeline can be tested before generation is added.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from config import DEFAULT_TOP_K, EMBEDDING_MODEL_NAME, PROMPT_DIR, RESULTS_DIR
from data_loader import load_all_processed_chunks
from chunking import create_chunks, format_chunk_for_display
from retrieval import EmbeddingRetriever

import json


Chunk = Dict[str, Any]
ANSWERS_DIR = RESULTS_DIR / "answers"


def load_system_prompt() -> str:
    prompt_path = PROMPT_DIR / "system_prompt.txt"
    return prompt_path.read_text(encoding="utf-8")


def build_rag_prompt(query: str, retrieved: List[Tuple[Chunk, float]]) -> str:
    """
    Build a prompt for a RAG-based answer.
    """
    system_prompt = load_system_prompt()

    context_blocks = []
    for rank, (chunk, score) in enumerate(retrieved, start=1):
        context_blocks.append(
            f"[Context {rank} | similarity={score:.4f}]\n"
            f"{format_chunk_for_display(chunk)}"
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""{system_prompt}

Retrieved context:
{context}

User question:
{query}

Answer:
"""
    return prompt


def generate_answer(prompt: str) -> str:
    """
    Placeholder language-model interface.

    Students must replace this with one of:
    - a local HuggingFace model;
    - an approved hosted API;
    - another justified SLM interface.

    The returned answer must be conditioned on the retrieved context.
    """
    # TODO: Replace this placeholder with a real model call.
    return (
        "[PLACEHOLDER ANSWER]\n"
        "Connect this function to your selected language model or API. "
        "Your final answer should use the retrieved context and should not invent unsupported details."
    )


def log_retrieval_results(history: List[Dict], query: str, answer: str, retrieved: List[Tuple[Chunk, float]]) -> None:
    """
    Log Q&A retrieval results into json structure.
    """
    # set up records structure
    current_entry = {
        "query": query,
        "answer": answer,
        "expected_focus": "",
        "question_type": "",
        "system": "",
        "retrieved_evidence": []
    }

    print("\nRetrieved evidence:")
    for rank, (chunk, score) in enumerate(retrieved, start=1):
        print("-" * 80)
        print(f"Rank {rank} | Score: {score:.4f}")
        print(format_chunk_for_display(chunk))

        # Checks for 'speakers' first, then 'speaker', defaults to ""
        speaker_info = chunk.get("speakers") or chunk.get("speaker") or ""

        # construct json records
        evidence_item = {
            "rank": rank,
            "score": round(float(score), 4),
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "play": chunk["play"],
            "act": chunk["act"],
            "scene": chunk["scene"],
            "scene_summary": chunk["scene_summary"],
            "speakers": speaker_info
        }
        current_entry["retrieved_evidence"].append(evidence_item)

    # save records into history
    history.append(current_entry)


def save_history(history: List[Dict], output_file: Any) -> None:
    """
    Save the Q&A retrieval results history to the output file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"All records has been saved as {output_file}")


def main() -> None:
    chunks = load_all_processed_chunks()
    retriever = EmbeddingRetriever(EMBEDDING_MODEL_NAME)

    if chunks:
        retriever.build_index(chunks)
        print("Index built successfully.")
    else:
        print("No valid data detected.")

    # make sure answers directory exists
    ANSWERS_DIR.mkdir(exist_ok=True)

    # define output file name
    OUTPUT_LOG_FILE = ANSWERS_DIR / "retrieval_history.json"
    q_and_a_history = []

    print("Shakespeare-aware RAG chatbot scaffold.")
    print("Type 'quit' to exit.\n")

    while True:
        query = input("Question: ").strip()
        if query.lower() in {"quit", "exit"}:
            save_history(q_and_a_history, OUTPUT_LOG_FILE)
            break

        retrieved = retriever.retrieve(query, top_k=DEFAULT_TOP_K)
        prompt = build_rag_prompt(query, retrieved)
        answer = generate_answer(prompt)

        log_retrieval_results(q_and_a_history, query, answer, retrieved)

        print("\nGenerated answer:")
        print(answer)
        print("\n")


if __name__ == "__main__":
    main()