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
# EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" # small, super fast Top 133
# EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"  Top 110
# EMBEDDING_MODEL_NAME = "intfloat/e5-base-v2" Top 97
# EMBEDDING_MODEL_NAME = "nomic-ai/nomic-embed-text-v1" # larger, but extremely slow on cpu Top 81
EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5" # large, balanced Top 66
# EMBEDDING_MODEL_NAME = "infgrad/Jasper-Token-Compression-600M" # Top 1 on MTEB Leaderboard 20260515,  but extremely slow on cpu
# EMBEDDING_MODEL_NAME = "jinaai/jina-embeddings-v5-text-nano" # Top 16 on MTEB Leaderboard

# Reranking
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"
# CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L12-v2"


# Lauguage Model
# LANGUAGE_MODEL_NAME = "distilgpt2"
# LANGUAGE_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
# LANGUAGE_MODEL_NAME = "microsoft/phi-2"
# LANGUAGE_MODEL_NAME = "google/gemma-3-270m-it"   # instruction-tuned version
LANGUAGE_MODEL_NAME = "google/gemma-3-1b-it"   # instruction-tuned version
# LANGUAGE_MODEL_NAME = "google/gemma-3-4b-it"   # instruction-tuned version


# Chunk Type
CHUNK_TYPE = "scenes"
# CHUNK_TYPE = "events"
# CHUNK_TYPE = "utterances"
# CHUNK_TYPE = "hybrid"