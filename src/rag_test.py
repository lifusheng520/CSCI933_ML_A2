"""
RAG Pipline Tester
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple, Optional
import json

from config import DEFAULT_TOP_K, EMBEDDING_MODEL_NAME, PROMPT_DIR, RESULTS_DIR, DATA_FILES
from data_loader import Record, load_jsonl
from chunking import format_chunk_for_display
from retrieval import EmbeddingRetriever
from baseline import baseline_answer
from gemma_models import GemmaAssistant

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

# def build_rag_prompt_event_chunk(query: str, retrieved: List[Tuple[Chunk, float]]) -> str:
#     """
#     Build a prompt for a RAG-based answer.
#     Ensures grounding, beginner-friendly explanation, and clear evidence usage.
#     """

#     system_prompt = load_system_prompt()

#     # -------------------------
#     # Format retrieved context
#     # -------------------------
#     context_blocks = []
#     for rank, (chunk, score) in enumerate(retrieved, start=1):
#         block = (
#             f"[Context {rank} | similarity={score:.4f}]\n"
#             f"Play: {chunk.get('play')}, Act {chunk.get('act')}, Scene {chunk.get('scene')}, Speaker: {chunk.get('speaker')}\n"
#             f"Scene Summary: {chunk.get('scene_summary')}\n"
#             f"Event Summary: {chunk.get('event_summary')}\n"
#             f"Text: {chunk.get('text')}"
#         )
#         context_blocks.append(block)

#     context = "\n\n".join(context_blocks)

#     # -------------------------
#     # Strong RAG instructions
#     # -------------------------
#     instructions = """
# You must follow these rules:
# 1. Answer ONLY using the retrieved context above.
# 2. Do NOT invent information not supported by the context.
# 3. If the context is insufficient, say "The provided context is insufficient to answer this question."
# 4. Explain clearly for a beginner with no prior knowledge of Shakespeare.
# 5. When possible, refer to Act/Scene in your explanation.
# 6. Keep the answer concise but informative.
# """

#     prompt = f"""{system_prompt}

# {instructions}

# ---------------------
# Retrieved Context:
# {context}
# ---------------------

# User Question:
# {query}

# Answer:
# """

#     return prompt

# def generate_answer(prompt: str, model_name:str = "distilgpt2") -> str:
#     """
#     Placeholder language-model interface.

#     Students must replace this with one of:
#     - a local HuggingFace model;
#     - an approved hosted API;
#     - another justified SLM interface.

#     The returned answer must be conditioned on the retrieved context.
#     """
#     answer = baseline_answer(prompt)
#     return (answer)

def log_retrieval_results(history: List[Dict], query: str, answer: str, retrieved: List[Tuple[Chunk, float]]) -> None:
    """
    Log Q&A retrieval results into json structure.
    """
    # set up records structure
    current_entry = {
        "query": query,
        "answer": answer,
        "retrieved_evidence": []
    }

    print("\nRetrieved evidence:")
    for rank, (chunk, score) in enumerate(retrieved, start=1):
        print("-" * 80)
        print(f"Rank {rank} | Score: {score:.4f}")
        print(format_chunk_for_display(chunk))

        # construct json records
        evidence_item = {
            "rank": rank,
            "score": round(float(score), 4),
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "play": chunk["play"],
            "act": chunk["act"],
            "scene": chunk["scene"],
            "speakers": chunk["speakers"]
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

def main(assistant) -> None:

    # load chunk datasets
    chunks = load_dataset_by_chunk_type()

    retriever = EmbeddingRetriever(EMBEDDING_MODEL_NAME)
    retriever.build_index(chunks)

    # make sure answers directory exists
    ANSWERS_DIR.mkdir(exist_ok=True)

    # define output file name
    OUTPUT_LOG_FILE = ANSWERS_DIR / "retrieval_history.json"
    q_and_a_history = []

    print("Shakespeare-aware RAG chatbot.")
    print("Type 'quit' to exit.\n")

    while True:
        query = input("Question: ").strip()
        if query.lower() in {"quit", "exit"}:
            save_history(q_and_a_history, OUTPUT_LOG_FILE)
            break

        retrieved = retriever.retrieve(query, top_k=DEFAULT_TOP_K)
        prompt = build_rag_prompt(query, retrieved)

        answer = assistant.generate_answer(prompt)

        log_retrieval_results(q_and_a_history, query, answer, retrieved)

        print("\nGenerated answer:")
        print(answer)
        print("\n")

def load_dataset_by_chunk_type(chunk_type: str = "events") -> List[Record]:
    """
    Load records from all JSONL files whose filename contains `chunk_type`
    (e.g. 'hybrid', 'scene', 'event', 'utterance').

    Args:
        folder_path: directory containing jsonl files
        keyword: substring filter for filenames

    Returns:
        List of all records across matched files
    """

    all_records: List[Record] = []
    updated_paths = []

    for _, path in enumerate(DATA_FILES):
    
        name = path.name  # file name only

        # insert "_hybrid" before "_chunks"
        new_name = name.replace("_chunks", f"_{chunk_type}")

        updated_paths.append(path.with_name(new_name))

    for file_path in updated_paths:
        records = load_jsonl(file_path)
        all_records.extend(records)

    print(f"Loaded {len(all_records)} records from {len(updated_paths)} {chunk_type} files.")
    return all_records

if __name__ == "__main__":

    model_name = "google/gemma-3-270m-it"   # instruction-tuned version
    # model_name = "google/gemma-3-1b-it"   # instruction-tuned version
    # model_name = "google/gemma-3-4b-it"   # instruction-tuned version
    assistant = GemmaAssistant(model_name)
    main(assistant)