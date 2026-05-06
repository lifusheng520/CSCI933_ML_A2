"""
Data loading utilities.

This file assumes that the processed Shakespeare dataset is available in JSON format.

Expected examples:
1. A file containing a list of records:
   [
     {"play": "Macbeth", "act": 1, "scene": 3, "speaker": "MACBETH", "text": "..."}
   ]

2. A file containing a dictionary with a "records" or "scenes" key:
   {"records": [...]} or {"scenes": [...]}
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
from config import PROCESSED_DIR


Record = Dict[str, Any]


def load_jsonl(file_path: Path) -> List[Record]:
    """
    Load a JSONL file.
    Each line must contain one JSON object.
    """
    records = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            records.append(json.loads(line))

    return records


def normalize_chunk(record: Record) -> Record:
    """
    Normalize different chunk schemas into
    one consistent retrieval schema.
    """

    chunk_type = record.get("chunk_type", "unknown")

    # unified chunk id
    chunk_id = (
        record.get("chunk_id")
        or record.get("scene_id")
        or record.get("utterance_id")
        or record.get("event_id")
    )

    normalized = {
        # universal identifiers
        "chunk_id": chunk_id,
        "chunk_type": chunk_type,

        # core retrieval text
        "text": record.get("text", ""),

        # metadata
        "play": record.get("play"),
        "act": record.get("act"),
        "scene": record.get("scene"),
        "scene_id": record.get("scene_id"),

        # optional metadata
        "speaker": record.get("speaker"),
        "location": record.get("location"),
        "scene_summary": record.get("scene_summary"),
        "keywords": record.get("keywords", []),
    }

    return normalized


def load_dataset(file_list: List[Path]) -> List[Record]:
    """
    Load and normalize multiple chunk files.
    """

    all_records = []

    for path in file_list:
        records = load_jsonl(path)

        for r in records:
            all_records.append(normalize_chunk(r))

    return all_records


# FILTERING
def filter_by_chunk_type(
    records: List[Record],
    chunk_type: str
) -> List[Record]:
    """
    Filter records by chunk type.
    """
    return [
        r for r in records
        if r["chunk_type"] == chunk_type
    ]

if __name__ == "__main__":

    folder = Path(PROCESSED_DIR)
    files = list(folder.glob("*.jsonl"))

    records = load_dataset(files)

    print(f"Loaded {len(records)} records")

    print("\nFirst record:\n")
    print(json.dumps(records[0], indent=2, ensure_ascii=False))