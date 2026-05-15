"""
RAG Pipline Tester
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple
import json
from collections import Counter

from config import DEFAULT_TOP_K, EMBEDDING_MODEL_NAME, CROSS_ENCODER_MODEL, LANGUAGE_MODEL_NAME, PROMPT_DIR, RESULTS_DIR, DATA_FILES, CHUNK_TYPE
from data_loader import Record, load_jsonl
from chunking import format_chunk_for_display
from retrieval import EmbeddingRetriever
# from baseline import baseline_answer
from gemma_models import GemmaAssistant

Chunk = Dict[str, Any]
ANSWERS_DIR = RESULTS_DIR / "answers"

def load_system_prompt(file_name:str = "system_prompt.txt") -> str:
    prompt_path = PROMPT_DIR / file_name
    return prompt_path.read_text(encoding="utf-8")

def retrieve_play_background(play_names: List[str]) -> str:
    # metadata augmentation
    play_background_content=''
    most_common_item = Counter(play_names).most_common(1)
    if most_common_item:
        play_name = most_common_item[0][0]
        print(f"The play found is: {play_name}")
        
        # Read the metadata text file directly
        with open(f'data/processed/metadata_{play_name.lower().replace(" ", "_")}.txt', 'r', encoding='utf-8') as f:
            play_background_content = f.read()
    return play_background_content


def build_rag_prompt(query: str, retrieved: List[Tuple[Chunk, float]], prompt_type="factual") -> str:
    """
    Build a prompt for a RAG-based answer.
    prompt_type values, include "factual" and "stylised" , means generation using factual style or Shakespeare style.
    """
    system_prompt = load_system_prompt("system_prompt.txt")
    stylised_prompt = load_system_prompt("stylised_prompt.txt")

    context_blocks = []
    play_names = []
    for rank, (chunk, score) in enumerate(retrieved, start=1):
        play_names.append(chunk.get("play", ""))
        context_blocks.append(
            # f"[Context {rank} | similarity={score:.4f}]\n"
            f"{format_chunk_for_display(chunk)}"
        )

    context = "\n\n".join(context_blocks)

    play_background = retrieve_play_background(play_names)

    if prompt_type == "factual":
        prompt_temp = system_prompt
    else:
        prompt_temp = stylised_prompt
    prompt = f"""{prompt_temp}

Play background:
{play_background}

Retrieved context:
{context}

User question:
{query}

Answer:
"""
    return prompt

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

def main(assistant, chunk_type='events') -> None:

    # load chunk datasets
    chunks_scenes = []
    chunks_events = []
    if chunk_type == 'hybrid' or chunk_type == 'scenes':
        chunks_scenes = load_dataset_by_chunk_type(chunk_type="scenes") # scene level
    if chunk_type == 'hybrid' or chunk_type == 'events':    
        chunks_events = load_dataset_by_chunk_type(chunk_type="events") # event level
    chunks = chunks_scenes + chunks_events

    retriever = EmbeddingRetriever(EMBEDDING_MODEL_NAME, CROSS_ENCODER_MODEL)

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

    print("Shakespeare-aware RAG chatbot.")
    print("Type 'quit' to exit.\n")

    while True:
        query = input("Question: ").strip()
        if query.lower() in {"quit", "exit"}:
            save_history(q_and_a_history, OUTPUT_LOG_FILE)
            break   

        # Retrieve evidences
        retrieved_t = retriever.retrieve(query)

        # Re-ranking
        retrieved = retriever.reranking(query, retrieved_t, top_k=DEFAULT_TOP_K)
        # retrieved = retrieved_t

        # Detect stylised query by consine similarity
        is_stylised = retriever.is_stylized_query(query)
        print(f"\nStylised Query Detected: {is_stylised}")

        # Build prompt: factual response generation vs Shakespeare style generation
        if not is_stylised:

            prompt = build_rag_prompt(
                query=query,
                retrieved=retrieved,
                prompt_type="factual"
            )
        else:

            prompt = build_rag_prompt(
                query=query,
                retrieved=retrieved,
                prompt_type="stylised"
            )

        answer = assistant.generate_answer(prompt)
        # answer = "" # for debugging

        log_retrieval_results(q_and_a_history, query, answer, retrieved)

        print("\nGenerated answer:")
        print(answer)
        print("\n")

def load_dataset_by_chunk_type(chunk_type: str = "events") -> List[Record]:
    """
    Load records from all JSONL files whose filename contains `chunk_type`
    (e.g. 'scenes', 'events', 'utterances').

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


    assistant = GemmaAssistant(LANGUAGE_MODEL_NAME)
    main(assistant, CHUNK_TYPE)