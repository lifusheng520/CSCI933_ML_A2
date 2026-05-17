"""
Embedding and retrieval utilities.

The default implementation uses sentence-transformers for embeddings
and scikit-learn cosine similarity for retrieval.

Students may replace this with FAISS, Chroma, LlamaIndex, LangChain,
or another approved method, but must justify the design in the report.
"""

from __future__ import annotations

import pickle
from pathlib import Path
import numpy as np
import faiss 
import hashlib
import json

from typing import Any, Dict, List, Tuple
from sentence_transformers import SentenceTransformer, CrossEncoder, util
# import torch
# from transformers import AutoModel


Chunk = Dict[str, Any]


class EmbeddingRetriever:
    """
    Faiss-based embedding retriever.
    """

    def __init__(self, embedding_model_name: str, cross_encoder_model: str):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "Install sentence-transformers: pip install sentence-transformers"
            ) from exc
        
        # cache
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)

        self.embedding_cache_path = self.cache_dir / f"embeddings_{embedding_model_name.replace('/', '_')}.pkl"
        self.faiss_cache_path = self.cache_dir / f"faiss_{embedding_model_name.replace('/', '_')}.index"
        self.meta_cache_path = self.cache_dir / f"chunks_{embedding_model_name.replace('/', '_')}.pkl"        

        self.faiss = faiss

        # embedding
        print(f"loading embedding model...{embedding_model_name}")
        # for other models
        self.model = SentenceTransformer(embedding_model_name, device="cpu")

        # for jasper
        # self.model = SentenceTransformer(
        #     embedding_model_name,
        #     model_kwargs={
        #         "torch_dtype": torch.bfloat16,
        #         "attn_implementation": "sdpa",  # We support flash_attention_2; sdpa; eager
        #         "trust_remote_code": True
        #     },
        #     trust_remote_code=True,
        #     tokenizer_kwargs={"padding_side": "left"},
        #     device="cpu",
        # )

        # for ninja
        # self.model = AutoModel.from_pretrained(
        #     embedding_model_name,
        #     trust_remote_code=True,
        #     _attn_implementation="flash_attention_2",  # Recommended but optional
        #     dtype=torch.bfloat16,  # Recommended for GPUs
        # )
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.model = self.model.to(device=device)

        # reranking
        print(f"loading cross-encoder model...{cross_encoder_model}")
        self.reranker = CrossEncoder(
            cross_encoder_model
        )

        self.chunks: List[Chunk] = []
        self.embeddings: np.ndarray | None = None
        self.index = None

        # -------------------------------------------------
        # Stylised response intent detection
        # -------------------------------------------------

        self.style_threshold = 0.68

        self.style_keywords = [

            "shakespearean",
            "shakespeare style",
            "speak like shakespeare",
            "old english",
            "elizabethan",
            "poetic",
            "theatrical",
            "dramatic style",
            "stylised",
            "stylized"
        ]

        self.style_examples = [

            "Answer in Shakespearean style",
            "Speak like Shakespeare",
            "Respond like Shakespeare",
            "Write in Shakespeare style",
            "Use Shakespearean language",

            "Use old English",
            "Answer in Elizabethan English",
            "Write like an old play",

            "Make it poetic",
            "Make the response dramatic",
            "Use a theatrical tone",
            "Respond like a stage play",
            "Write dramatically",

            "Give a stylised response",
            "Provide a stylized Shakespeare response",
            "Answer with Shakespeare-like wording",

            "Couldst thou answer poetically",
            # "Make it sound like Macbeth",
            "Talk like a Shakespeare character",
            "Write as if from a Shakespeare play"
        ]

        # Precompute embeddings once
        self.style_embeddings = self.model.encode(
            self.style_examples,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def save_cache(self) -> None:
        """
        Save embeddings, FAISS index, and chunks to disk.
        """

        if self.index is None or self.embeddings is None:
            raise RuntimeError("Nothing to cache. Build index first.")

        # Save FAISS index
        faiss.write_index(self.index, str(self.faiss_cache_path))

        # Save embeddings + chunks + model info
        with open(self.embedding_cache_path, "wb") as f:
            pickle.dump(self.embeddings, f)

        with open(self.meta_cache_path, "wb") as f:
            pickle.dump(self.chunks, f)

        print("Cache saved successfully.")

    def load_cache(self) -> bool:
        """
        Load FAISS index + embeddings if available.
        Returns True if cache loaded successfully.
        """

        if not (
            self.faiss_cache_path.exists()
            and self.embedding_cache_path.exists()
            and self.meta_cache_path.exists()
        ):
            return False

        # Load FAISS index
        self.index = faiss.read_index(str(self.faiss_cache_path))

        # Load embeddings
        with open(self.embedding_cache_path, "rb") as f:
            self.embeddings = pickle.load(f)

        # Load chunks
        with open(self.meta_cache_path, "rb") as f:
            self.chunks = pickle.load(f)

        print("Cache loaded successfully.")
        return True        

    def _get_text(self, chunk):

        import re

        text = chunk["text"]

        # Scene Chunk
        match = re.search(r"Scene text:(.*)", text, re.DOTALL)

        if not match:
            # Event Chunk
            match = re.search(r"Event dialogue:(.*)", text, re.DOTALL)

        dialogue = match.group(1).strip() if match else ""

        # print(dialogue)
        return dialogue

    def _build_retrieval_text(self, chunk: Chunk) -> str:
        """
        Text used for embedding/retrieval.
        """
        return f"""
        Play: {chunk.get("play", "")}

        Act: {chunk.get("act", "")}
        
        Scene: {chunk.get("scene", "")}

        Keywords:
        {chunk.get("keywords", "")}

        Speaker:
        {chunk.get("speaker", "")}

        Scene summary:
        {chunk.get("scene_summary", "")}

        Dialogue:
        {self._get_text(chunk)}
        """        

        # {self._get_text(chunk)[:300]}

    def build_index(self, chunks: List[Chunk]) -> None:
        """
        Create FAISS index from embeddings.
        Save and load cache.
        """
        if not chunks:
            raise ValueError("No chunks supplied to build_index().")
        
        print("Checking cache...")

        if self.cache_is_valid(chunks):
            print("Cache is valid. Loading index from disk...")

            loaded = self.load_cache()

            if loaded:
                print("✅ Cache loaded successfully.")
                return

            print("⚠️ Cache validation passed but loading failed. Rebuilding...")

        else:
            print("Building index...")    
        
        self.chunks = chunks

        # indexing by texts
        # retrieval_texts = [chunk["text"] for chunk in chunks]

        # indexing by summaries, but not retrieve all
        retrieval_texts = [
            self._build_retrieval_text(chunk)
            for chunk in chunks
        ]

        # for others
        embeddings = self.model.encode(
            retrieval_texts,
            show_progress_bar=True,
            batch_size=32,
            convert_to_numpy=True,
            device="cpu",
            normalize_embeddings=True
        )

        # for ninja
        # embeddings = self.model.encode(
        #     texts=retrieval_texts,
        #     task="retrieval",
        #     prompt_name="query",
        # )
        # faiss.normalize_L2(embeddings)         # Normalize embeddings → cosine similarity via inner product

        self.embeddings = embeddings

        dim = embeddings.shape[1]

        # Inner product index (cosine after normalization)
        self.index = self.faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        # save everything
        self.save_cache()
        self.save_manifest(self._compute_dataset_hash(chunks))     

        print(f"Indexed and cached {len(chunks)} chunks.")

    def _compute_dataset_hash(self, chunks: List[Chunk]) -> str:
        """
        Compute a deterministic hash for the dataset used in FAISS indexing.
        """

        normalized = []

        for c in chunks:
            normalized.append({
                "play": c.get("play", ""),
                "act": c.get("act", ""),
                "scene": c.get("scene", ""),
                "text": c.get("text", ""),
                "scene_summary": c.get("scene_summary", "")
            })

        # ensure stable ordering
        serialized = json.dumps(normalized, sort_keys=True).encode("utf-8")

        return hashlib.sha256(serialized).hexdigest()

    def cache_is_valid(self, chunks: List[Chunk]) -> bool:
        expected_hash = self._compute_dataset_hash(chunks)

        manifest_path = self.cache_dir / "manifest.json"

        if not manifest_path.exists():
            return False

        with open(manifest_path, "r") as f:
            meta = json.load(f)

        return meta.get("dataset_hash") == expected_hash
    
    def save_manifest(self, dataset_hash: str) -> None:
        manifest_path = self.cache_dir / "manifest.json"

        meta = {
            "dataset_hash": dataset_hash,
            "embedding_model": str(self.model),
            "num_chunks": len(self.chunks)
        }

        with open(manifest_path, "w") as f:
            json.dump(meta, f, indent=2)

    def retrieve(self, query: str, top_k: int = 20) -> List[Tuple[Chunk, float]]:
        """
        Retrieve top-k chunks using FAISS.
        """
        if self.index is None:
            raise RuntimeError("Index not built. Call build_index() first.")

        # for bge
        instruction = "Represent this sentence for searching relevant passages:" # BGE embedding instruction
        query_embedding = np.array(self.model.encode(
            [instruction + query], 
            normalize_embeddings=True))
        
        # for ninja
        # query_embedding = self.model.encode(
        #     texts=query,
        #     task="retrieval",
        #     prompt_name="query",
        # )
        # self.faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            chunk = self.chunks[idx].copy()
            # Remove redundant information
            chunk['text'] = 'Dialogue Text: ' + self._get_text(chunk)
            # IMPORTANT: keep evidence structured for RAG report
            results.append((chunk, float(score)))

        return results
    

    def reranking(self, query: str, results: List[Tuple[Chunk, float]], top_k: int = 3) -> List[Tuple[Chunk, float]]:
        """
        Rerank retrieved chunks using CrossEncoder.

        Args:
            query: user query
            results: FAISS retrieval results
                     [(chunk, similarity_score), ...]
            top_k: number of final reranked results

        Returns:
            List[(chunk, rerank_score)]
        """

        if not results:
            return []

        # Build query-document pairs
        pairs = [
            (
                query,
                self._build_retrieval_text(chunk)
            )
            for chunk, _ in results
        ]

        # Predict relevance scores
        scores = self.reranker.predict(pairs)

        # Combine chunk with reranker score
        reranked = []

        for (chunk, _old_score), rerank_score in zip(results, scores):

            reranked.append(
                (chunk, float(rerank_score))
            )

        # Sort descending
        reranked.sort(
            key=lambda x: x[1],
            reverse=True
        )

        # Return top-k
        return reranked[:top_k]
    
    # Stylised response intent detection
    def _keyword_style_match(self, query: str) -> bool:
        """
        Fast keyword-based style detection.
        """

        query_lower = query.lower()

        return any(
            keyword in query_lower
            for keyword in self.style_keywords
        )

    def style_similarity(self, query: str) -> float:
        """
        Compute similarity between user query
        and stylised-example questions.
        """

        # Encode query
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        # Cosine similarity
        similarities = np.dot(
            self.style_embeddings,
            query_embedding.T
        ).squeeze()

        # Max similarity
        max_score = float(np.max(similarities))

        return max_score

    def is_stylized_query(self, query: str) -> bool:
        """
        Determine whether user requests a stylised response.

        Uses:
        1. keyword matching
        2. embedding similarity
        """

        # Fast keyword shortcut
        if self._keyword_style_match(query):
            return True

        similarity = self.style_similarity(query)

        return similarity >= self.style_threshold

    def debug_style_detection(self, query: str) -> None:
        """
        Debug helper for tuning similarity threshold.
        """

        similarity = self.style_similarity(query)

        print("=" * 60)
        print(f"Query: {query}")
        print(f"Similarity: {similarity:.4f}")
        print(f"Threshold: {self.style_threshold:.4f}")
        print(
            f"Stylised detected: "
            f"{similarity >= self.style_threshold}"
        )
        print("=" * 60)