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
from data_loader import load_dataset
from chunking import create_chunks
from retrieval import EmbeddingRetriever

def build_index():
    print("Loading dataset...")
    
    # will change to this code after we decide which strategy should be used
    #records = load_dataset(DATA_FILES)

    # for now we get all jsonl files
    folder = Path(PROCESSED_DIR)
    data_files = list(folder.glob("*.jsonl"))
    records = load_dataset(data_files)

    print("Creating chunks...")
    chunks = create_chunks(records)

    texts = [c["text"] for c in chunks]

    metadata = []
    for c in chunks:
        metadata.append({
            "chunk_id": c["chunk_id"],
            "play": c["play"],
            "act": c["act"],
            "scene": c["scene"],
            "speaker": c["speaker"]
        })

    print("Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("Encoding chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)

    print("Saving index...")

    INDEX_DIR.mkdir(exist_ok=True)

    np.save(INDEX_DIR / "embeddings.npy", embeddings)

    with open(INDEX_DIR / "texts.pkl", "wb") as f:
        pickle.dump(texts, f)

    with open(INDEX_DIR / "metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("Index built successfully!")

def retrieve(query, top_k=DEFAULT_TOP_K):
    print("Loading index...")

    embeddings = np.load(INDEX_DIR / "embeddings.npy")

    with open(INDEX_DIR / "texts.pkl", "rb") as f:
        texts = pickle.load(f)

    with open(INDEX_DIR / "metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    query_vec = model.encode([query])[0]

    # cosine similarity
    scores = embeddings @ query_vec / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_vec)
    )

    top_indices = np.argsort(scores)[-top_k:][::-1]

    retrieved_chunks = []
    for idx in top_indices:
        retrieved_chunks.append({
            "text": texts[idx],
            "metadata": metadata[idx],
            "score": float(scores[idx])
        })

    return retrieved_chunks

def main() -> None:
    build_index()

    print("\nTest retrieval:\n")

    results = retrieve("Why does Macbeth kill Duncan?")

    for r in results:
        print("\n---")
        print(r["metadata"])
        print(r["text"][:200])


if __name__ == "__main__":
    main()
