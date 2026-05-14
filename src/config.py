"""
Configuration for the Assignment 2 starter code.

Students should adjust these values to match their own implementation.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" 
PROCESSED_DIR = DATA_DIR / "processed"
RAW_DIR = DATA_DIR/ "raw"

INDEX_DIR = PROJECT_ROOT / "index"
PROMPT_DIR = PROJECT_ROOT / "prompts"
RESULTS_DIR = PROJECT_ROOT / "results"
QUESTIONS_DIR = PROJECT_ROOT / "questions"

PLAY_FILES = {
    "hamlet": RAW_DIR / "hamlet.json",
    "macbeth": RAW_DIR / "macbeth.json",
    "romeo_and_juliet": RAW_DIR / "romeo_and_juliet.json",
}

DATA_FILES = [
    PROCESSED_DIR / "hamlet_chunks.jsonl",
    PROCESSED_DIR / "macbeth_chunks.jsonl",
    PROCESSED_DIR / "romeo_and_juliet_chunks.jsonl"
]

CHUNK_TYPES = ["scene", "utterance", "event"]

DEFAULT_TOP_K = 3

# Suggested lightweight embedding model.
# Students may change this and justify the choice in the report.
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


