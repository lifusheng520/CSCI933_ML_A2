"""
Build and test a simple retrieval index.

This script is a sanity check that:
1. the dataset can be loaded;
2. chunks can be created;
3. embeddings can be generated;
4. retrieval returns plausible passages.
"""
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

from config import *
from chunking import create_chunks, load_play_json, format_chunk_for_display
from data_loader import load_dataset
from retrieval import EmbeddingRetriever

def main() -> None:
    # create folder if not exist
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    total_records = 0
    for play_key, input_path in PLAY_FILES.items():
        print(f"Processing {play_key}...")
        
        # load plays
        records = load_play_json(input_path)
        total_records += len(records)

        # create chunks
        create_chunks(play_key, records)

    print("Chunking complete.")
    
    retriever = EmbeddingRetriever(EMBEDDING_MODEL_NAME)
    print("Loading dataset...")

    for chunk_type in CHUNK_TYPES:
        print(f"Chunk Type: {chunk_type.capitalize()}")
        folder = Path(PROCESSED_DIR)
        data_files = list(folder.glob(f"*{chunk_type}s.jsonl"))
        chunks = load_dataset(data_files)

        #print(f"Loaded {total_records} records.")
        print(f"Created {len(chunks)} retrieval chunks.")

        retriever.build_index(chunks)

        query = "Why does Macbeth kill Duncan?"
        results = retriever.retrieve(query, top_k=DEFAULT_TOP_K)

        print("\nQuery:", query)
        print("\nTop retrieved chunks:\n")

        for rank, (chunk, score) in enumerate(results, start=1):
            print("=" * 80)
            print(f"Rank {rank} | Score: {score:.4f}")
            print(format_chunk_for_display(chunk))

if __name__ == "__main__":
    main()
