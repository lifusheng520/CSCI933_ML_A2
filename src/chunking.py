"""
Chunking utilities.

Students should implement and justify a chunking strategy.
This starter file provides a simple default: one input record becomes one retrieval chunk.
"""

from __future__ import annotations

from typing import Any, Dict, List


Record = Dict[str, Any]
Chunk = Dict[str, Any]


def _get_text(record: Record) -> str:
    """
    Extract text from a record using common field names.
    Adapt this function if your dataset uses different names.
    """
    for key in ["text", "utterance", "excerpt", "content", "passage"]:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    # Fallback: combine selected fields if no obvious text field exists.
    parts = []
    for key in ["speaker", "summary", "modern_summary"]:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())

    return " ".join(parts).strip()


def create_chunks(records):
    """
    Starter function — now adapted for already chunked data
    """
    chunks = []

    for r in records:
        chunk = {
            "chunk_id": r["chunk_id"],
            "text": enrich_text(r),
            "play": r["play"],
            "act": r["act"],
            "scene": r["scene"],
            "speaker": r["speaker"]
        }
        chunks.append(chunk)

    return chunks


def enrich_text(record):
    """
    Improve retrieval quality using metadata
    """
    text = record["text"]

    # Add scene summary if available
    if "scene_summary" in record and record["scene_summary"]:
        text = record["scene_summary"] + " " + text

    return text


def format_chunk_for_display(chunk: Chunk) -> str:
    """
    Format a retrieved chunk for display to the user.
    """
    play = chunk.get("play", "Unknown play")
    act = chunk.get("act", "?")
    scene = chunk.get("scene", "?")
    speaker = chunk.get("speaker", "")

    header = f"{play}, Act {act}, Scene {scene}"
    if speaker:
        header += f", Speaker: {speaker}"

    return f"[{header}]\n{chunk.get('text', '')}"
