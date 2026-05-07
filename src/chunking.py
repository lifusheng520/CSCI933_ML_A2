"""
Chunking utilities.

Chunking strategies:
1. Scene
2. Utterances
3. Events
"""

from __future__ import annotations
from pathlib import Path
import re
import json
from typing import Any, Dict, List
from config import PLAY_FILES, PROCESSED_DIR


Record = Dict[str, Any]
Chunk = Dict[str, Any]

# BASIC UTILITIES
def _get_text(record: Record) -> str:
    value = record.get("text", "")
    if isinstance(value, str):
        return clean_text(value)
    return ""

def clean_text(text: str) -> str:
    """
    Normalize whitespace without changing content meaning.
    """
    return " ".join(str(text).split()).strip()


def is_valid_text(text: str) -> bool:
    """
    Skip empty text only.
    Do not generate or infer new meaning here.
    """
    return bool(clean_text(text))


def load_play_json(path: Path) -> Record:
    """
    Load JSON.
    Expected structure:
    {
      "metadata": {...},
      "scenes": [...]
    }
    """
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if "scenes" not in data:
        raise ValueError(f"Expected key 'scenes' in {path}")

    return data


def write_jsonl(path: Path, records: List[Record]) -> None:
    """
    Write one JSON object per line.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def format_chunk_for_display(chunk: Chunk) -> str:
    """
    Format a retrieved chunk for display to the user.
    """
    play = chunk.get("play", "Unknown play")
    act = chunk.get("act", "?")
    scene = chunk.get("scene", "?")
    speaker = chunk.get("speaker", "")
    scene_summary = chunk.get("scene_summary", "")
    event_summary = chunk.get("event_summary", "")
    #chunk_type = chunk.get("chunk_type")

    #header = f"{play}, Act {act}, Scene {scene}, Chunk Type: {chunk_type}"
    header = f"{play}, Act {act}, Scene {scene}"
    if speaker:
        header += f", Speaker: {speaker}"
    if scene_summary:
        header += f", Scene Summary: {scene_summary}"
    if event_summary:
        header += f", Event Summary: {event_summary}"

    return f"[{header}]\n{chunk.get('text', '')}"

# SHARED METADATA

def scene_metadata(scene: Record) -> Record:
    """
    Shared metadata for all chunking strategies
    """
    return {
        "play": scene.get("play"),
        "act": scene.get("act"),
        "scene": scene.get("scene"),
        "scene_id": scene.get("scene_id"),
        "location": scene.get("location", ""),
        "scene_summary": scene.get("scene_summary", ""),
        "keywords": scene.get("keywords", []),
    }

# BUILD TEXT
def build_scene_text(scene: Record) -> str:
    meta = scene_metadata(scene)

    parts = [
        f"Play: {meta['play']}.",
        f"Act {meta['act']}, Scene {meta['scene']}.",
    ]

    if meta["location"]:
        parts.append(f"Location: {meta['location']}.")

    if meta["scene_summary"]:
        parts.append(f"Scene summary: {meta['scene_summary']}.")

    if meta["keywords"]:
        parts.append(f"Keywords: {', '.join(meta['keywords'])}.")

    parts.append(f"Scene text: {_get_text(scene)}")

    return clean_text(" ".join(parts))


def build_utterance_text(scene: Record, utterance: Record) -> str:
    meta = scene_metadata(scene)

    parts = [
        f"Play: {meta['play']}.",
        f"Act {meta['act']}, Scene {meta['scene']}.",
    ]

    if meta["scene_summary"]:
        parts.append(f"Scene summary: {meta['scene_summary']}.")

    if meta["keywords"]:
        parts.append(f"Keywords: {', '.join(meta['keywords'])}.")

    parts.append(f"Speaker: {utterance.get('speaker')}.")
    parts.append(f"Dialogue: {_get_text(utterance)}")

    return clean_text(" ".join(parts))


def build_event_text(scene: Record, display_text: str, speakers: List[str]) -> str:
    meta = scene_metadata(scene)

    parts = [
        f"Play: {meta['play']}.",
        f"Act {meta['act']}, Scene {meta['scene']}.",
    ]

    if meta["location"]:
        parts.append(f"Location: {meta['location']}.")

    if meta["scene_summary"]:
        parts.append(f"Scene summary: {meta['scene_summary']}.")

    if meta["keywords"]:
        parts.append(f"Keywords: {', '.join(meta['keywords'])}.")

    if speakers:
        parts.append(f"Speakers: {', '.join(speakers)}.")

    parts.append(f"Event dialogue: {display_text}")

    return clean_text(" ".join(parts))

# STRATEGY 1: SCENE CHUNKS
def create_scene_chunks(records: List[Record]) -> List[Record]:
    """
    One chunk per scene.
    Best for broad narrative/context questions.
    """
    chunks = []

    for record in records:
        text = build_scene_text(record)

        if not is_valid_text(text):
            continue

        meta = scene_metadata(record)

        chunks.append({
            "chunk_type": "scene",
            "chunk_id": meta["scene_id"],
            "source_id": meta["scene_id"],
            **meta,
            "text": text,
        })

    return chunks


# STRATEGY 2: UTTERANCE CHUNKS
def create_utterance_chunks(records: List[Record]) -> List[Record]:
    """
    One chunk per speaker turn.
    Best for quote lookup and speaker-specific questions.
    """
    chunks = []

    for record in records:
        meta = scene_metadata(record)

        for utterance in record.get("utterances", []):
            text = build_utterance_text(record, utterance)

            if not is_valid_text(text):
                continue

            utterance_id = (
                utterance.get("utterance_id")
                or utterance.get("source_id")
                or f"{meta['scene_id']}_{len(chunks) + 1:04d}"
            )

            chunks.append({
                "chunk_type": "utterance",
                "chunk_id": utterance_id,
                "utterance_id": utterance_id,
                "source_id": utterance.get("source_id", utterance_id),
                **meta,
                "speaker": utterance.get("speaker"),
                "speaker_original": utterance.get("speaker_original"),
                "text": text
            })

    return chunks


# STRATEGY 3: EVENT CHUNKS
def create_event_chunks(
    records: List[Record],
    group_size: int = 8,
    overlap: int = 2,
) -> List[Record]:
    """
    Semantically meaningful passage chunks approximated by grouped speaker turns.

    group_size: Number of utterances per event chunk.
    overlap: Number of utterances repeated between adjacent event chunks.
    """
    chunks = []

    if overlap >= group_size:
        raise ValueError("overlap must be smaller than group_size")

    for record in records:
        meta = scene_metadata(record)

        utterances = [
            u for u in record.get("utterances", [])
            if is_valid_text(u.get("text", ""))
        ]

        if not utterances:
            continue

        step = group_size - overlap
        event_num = 1

        for start in range(0, len(utterances), step):
            group = utterances[start:start + group_size]

            if len(group) < 2:
                continue

            event_id = f"{meta['scene_id']}_event_{event_num:04d}"

            speakers = []
            lines = []

            for u in group:
                speaker = u.get("speaker", "UNKNOWN")
                text = clean_text(_get_text(u))

                if speaker != "STAGE_DIRECTION" and speaker not in speakers:
                    speakers.append(speaker)

                lines.append(f"{speaker}: {text}")

            display_text = "\n".join(lines)
            text = build_event_text(record, display_text, speakers)

            chunks.append({
                "chunk_type": "event",
                "chunk_id": event_id,
                "event_id": event_id,
                "source_id": event_id,
                **meta,
                "speakers": speakers,
                "event_summary": meta["scene_summary"],
                "text": text
            })

            event_num += 1

    return chunks


# MAIN PIPELINE
def create_chunks(play_key: str, records) -> None:
    scenes = records["scenes"]

    scene_chunks = create_scene_chunks(scenes)
    utterance_chunks = create_utterance_chunks(scenes)
    event_chunks = create_event_chunks(scenes)

    write_jsonl(PROCESSED_DIR / f"{play_key}_scenes.jsonl", scene_chunks)
    write_jsonl(PROCESSED_DIR / f"{play_key}_utterances.jsonl", utterance_chunks)
    write_jsonl(PROCESSED_DIR / f"{play_key}_events.jsonl", event_chunks)

    print(f"  scene chunks: {len(scene_chunks)}")
    print(f"  utterance chunks: {len(utterance_chunks)}")
    print(f"  event chunks: {len(event_chunks)}")


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for play_key, input_path in PLAY_FILES.items():
        print(f"Processing {play_key}...")
        record = load_play_json(input_path)
        create_chunks(play_key, record)

    print("Chunking complete.")


if __name__ == "__main__":
    main()