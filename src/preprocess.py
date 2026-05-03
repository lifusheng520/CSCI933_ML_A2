import json
import os
from config import *


# -------------------------
# LOAD JSONL
# -------------------------
def load_jsonl(file_path):
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    return records


# -------------------------
# CLEAN
# -------------------------
def clean_records(records):
    cleaned = []

    for r in records:
        speaker = r["speaker"].strip().upper()

        is_stage = speaker == "STAGE_DIRECTION"

        if speaker in ["ELSINORE", "VERONA", "PARIS HOUSE"]:
            continue

        cleaned.append({
            "play": r["play"],
            "act": r["act"],
            "scene": r["scene"],
            "speaker": speaker,
            "utterance": r["text"].strip(),
            "source_id": r["source_id"],
            "scene_summary": r.get("scene_summary", ""),
            "keywords": r.get("keywords", []),
            "is_stage_direction": is_stage
        })

    return cleaned


# -------------------------
# CHUNK STRATEGIES
# -------------------------

# UTTERANCE LEVEL
def chunk_utterance(records):
    chunks = []

    for r in records:
        chunks.append({
            "chunk_id": r["source_id"],
            "text": r["utterance"],
            "play": r["play"],
            "act": r["act"],
            "scene": r["scene"],
            "speaker": r["speaker"]
        })

    return chunks


# SPEAKER GROUPING (DEFAULT)
def chunk_speaker(records):
    chunks = []
    buffer = None

    for r in records:
        if buffer is None:
            buffer = r.copy()
            continue

        if (
            r["speaker"] == buffer["speaker"]
            and r["act"] == buffer["act"]
            and r["scene"] == buffer["scene"]
        ):
            buffer["utterance"] += " " + r["utterance"]
        else:
            chunks.append(create_chunk(buffer))
            buffer = r.copy()

    if buffer:
        chunks.append(create_chunk(buffer))

    return chunks


# SCENE LEVEL
def chunk_scene(records):
    chunks = []
    grouped = {}

    for r in records:
        key = (r["play"], r["act"], r["scene"])

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(r["utterance"])

    for (play, act, scene), utterances in grouped.items():
        chunks.append({
            "chunk_id": f"{play}_{act}_{scene}_scene",
            "text": " ".join(utterances),
            "play": play,
            "act": act,
            "scene": scene,
            "speaker": "MULTI"
        })

    return chunks


# HYBRID
def chunk_hybrid(records):
    """
    Speaker chunk + scene summary + keyword boost
    """
    speaker_chunks = chunk_speaker(records)
    enriched = []

    for c in speaker_chunks:
        text = c["text"]

        # find original record for metadata
        for r in records:
            if r["play"] == c["play"] and r["act"] == c["act"] and r["scene"] == c["scene"]:
                summary = r.get("scene_summary", "")
                keywords = r.get("keywords", [])

                if summary:
                    text = summary + " " + text

                if keywords:
                    text = text + " " + " ".join(keywords)

                break

        new_chunk = c.copy()
        new_chunk["text"] = text

        enriched.append(new_chunk)

    return enriched


# -------------------------
# HELPER
# -------------------------
def create_chunk(record):
    return {
        "chunk_id": record["source_id"],
        "text": record["utterance"],
        "play": record["play"],
        "act": record["act"],
        "scene": record["scene"],
        "speaker": record["speaker"]
    }


# -------------------------
# SAVE
# -------------------------
def save_jsonl(data, path):
    with open(path, "w", encoding="utf-8") as f:
        for r in data:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


# -------------------------
# MAIN PIPELINE
# -------------------------
def process_dataset(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith("_utterances.jsonl"):
            play_name = file.replace("_utterances.jsonl", "")

            print(f"\nProcessing {play_name}...")

            records = load_jsonl(os.path.join(input_dir, file))
            cleaned = clean_records(records)

            # -------------------------
            # APPLY ALL STRATEGIES
            # -------------------------
            utterance_chunks = chunk_utterance(cleaned)
            speaker_chunks = chunk_speaker(cleaned)
            scene_chunks = chunk_scene(cleaned)
            hybrid_chunks = chunk_hybrid(cleaned)

            # -------------------------
            # SAVE ALL
            # -------------------------
            save_jsonl(utterance_chunks, os.path.join(output_dir, f"{play_name}_utterance_chunks.jsonl"))
            save_jsonl(speaker_chunks, os.path.join(output_dir, f"{play_name}_speaker_chunks.jsonl"))
            save_jsonl(scene_chunks, os.path.join(output_dir, f"{play_name}_scene_chunks.jsonl"))
            save_jsonl(hybrid_chunks, os.path.join(output_dir, f"{play_name}_hybrid_chunks.jsonl"))

            print(f"{play_name}:")
            print(f"  utterance: {len(utterance_chunks)}")
            print(f"  speaker:   {len(speaker_chunks)}")
            print(f"  scene:     {len(scene_chunks)}")
            print(f"  hybrid:    {len(hybrid_chunks)}")


if __name__ == "__main__":
    process_dataset(
        input_dir=RAW_DIR,
        output_dir=PROCESSED_DIR
    )