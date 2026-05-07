"""
Embedding and retrieval utilities.

The default implementation uses sentence-transformers for embeddings
and scikit-learn cosine similarity for retrieval.

Students may replace this with FAISS, Chroma, LlamaIndex, LangChain,
or another approved method, but must justify the design in the report.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple
from sentence_transformers import SentenceTransformer

import numpy as np
import faiss 


Chunk = Dict[str, Any]


class EmbeddingRetriever:
    """
    Faiss-based embedding retriever.
    """

    def __init__(self, embedding_model_name: str):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "Install sentence-transformers: pip install sentence-transformers"
            ) from exc

        self.faiss = faiss
        self.model = SentenceTransformer(embedding_model_name, device="cpu")

        self.chunks: List[Chunk] = []
        self.embeddings: np.ndarray | None = None
        self.index = None

    def _build_retrieval_text(self, chunk: Chunk) -> str:
        """
        Text used for embedding/retrieval.
        """

        return f"""
        Play: {chunk.get("play", "")}

        Scene summary:
        {chunk.get("scene_summary", "")}

        Event summary:
        {chunk.get("event_summary", "")}

        Speaker:
        {chunk.get("speaker", "")}

        Text preview:
        {chunk.get("text", "")[:300]}
        """

    def build_index(self, chunks: List[Chunk]) -> None:
        """
        Create FAISS index from embeddings.
        """
        if not chunks:
            raise ValueError("No chunks supplied to build_index().")

        self.chunks = chunks
        
        # indexing by texts
        # retrieval_texts = [chunk["text"] for chunk in chunks]

        # indexing by summaries, but retrieve all
        retrieval_texts = [
            self._build_retrieval_text(chunk)
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            retrieval_texts,
            show_progress_bar=True,
            batch_size=32,
            convert_to_numpy=True,
            device="cpu"
        )

        # Normalize embeddings → cosine similarity via inner product
        faiss.normalize_L2(embeddings)

        self.embeddings = embeddings

        dim = embeddings.shape[1]

        # Inner product index (cosine after normalization)
        self.index = self.faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        print(f"Indexed {len(chunks)} chunks.")

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Chunk, float]]:
        """
        Retrieve top-k chunks using FAISS.
        """
        if self.index is None:
            raise RuntimeError("Index not built. Call build_index() first.")

        query_embedding = np.array(self.model.encode([query]))
        self.faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            chunk = self.chunks[idx]

            # IMPORTANT: keep evidence structured for RAG report
            results.append((chunk, float(score)))

        return results
