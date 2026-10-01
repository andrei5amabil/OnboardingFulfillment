import pickle
import re
from pathlib import Path
from typing import Any
from sentence_transformers import CrossEncoder

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Anchor paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_PATH = PROJECT_ROOT / "chroma_db"
BM25_INDEX_PATH = CHROMA_PATH / "bm25_index.pkl"
COLLECTION_NAME = "policies"

RRF_K = 60  # Standard RRF constant smoothing parameter


def tokenize_for_bm25(text: str) -> list[str]:
    """Preserves clause tags and alphanumeric words identically to ETL."""
    return re.findall(r"[a-zA-Z0-9_\-]+", text.lower())


class PolicyRetriever:

    def __init__(self):
        if not CHROMA_PATH.exists() or not BM25_INDEX_PATH.exists():
            raise FileNotFoundError(
                f"Index files missing at {CHROMA_PATH}. Run 'python src/rag/etl.py' first."
            )

        # 1. Initialize LangChain Chroma vector store & dense embedder
        self.embed_fn = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embed_fn,
            persist_directory=str(CHROMA_PATH),
        )

        # 2. Load serialized BM25 index & corpus map
        with open(BM25_INDEX_PATH, "rb") as f:
            bm25_data = pickle.load(f)
            self.bm25 = bm25_data["model"]
            self.doc_ids = bm25_data["ids"]
            self.documents = bm25_data["documents"]
            self.metadatas = bm25_data["metadatas"]
            self.parent_store = bm25_data.get("parent_store", {})

        # Fast lookup mapping child_id -> index
        self.id_to_idx = {doc_id: idx for idx, doc_id in enumerate(self.doc_ids)}

        # 3. Load lightweight Cross-Encoder for precision reranking
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def _dense_search(self, query: str, top_k: int = 15) -> list[tuple[str, int]]:
        """Dense semantic search using LangChain Chroma cosine similarity."""
        docs = self.vector_store.similarity_search(query, k=top_k)
        
        return [
            (doc.id or doc.metadata.get("id"), rank + 1)
            for rank, doc in enumerate(docs)
            if doc.id or doc.metadata.get("id")
        ]

    def _sparse_search(self, query: str, top_k: int = 15) -> list[tuple[str, int]]:
        """Exact keyword matching using BM25Okapi."""
        tokens = tokenize_for_bm25(query)
        if not tokens:
            return []

        scores = self.bm25.get_scores(tokens)
        top_indices = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )[:top_k]

        # Return tuples of (chunk_id, 1-based rank)
        return [
            (self.doc_ids[idx], rank + 1)
            for rank, idx in enumerate(top_indices)
            if scores[idx] > 0
        ]

    def _reciprocal_rank_fusion(
        self,
        dense_ranks: list[tuple[str, int]],
        sparse_ranks: list[tuple[str, int]],
        top_k: int = 10,
    ) -> list[str]:
        """Calculates RRF score: Sum(1 / (RRF_K + rank)) across modalities."""
        rrf_scores: dict[str, float] = {}

        for doc_id, rank in dense_ranks:
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (
                1.0 / (RRF_K + rank)
            )

        for doc_id, rank in sparse_ranks:
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (
                1.0 / (RRF_K + rank)
            )

        # Sort candidate child IDs descending by combined RRF score
        sorted_docs = sorted(
            rrf_scores.items(), key=lambda item: item[1], reverse=True
        )
        return [doc_id for doc_id, _ in sorted_docs[:top_k]]

    def retrieve(
        self,
        query: str,
        top_k_candidates: int = 12,
        final_top_k: int = 3,
    ) -> list[dict[str, Any]]:
        """Orchestrates Hybrid Search -> RRF -> Cross-Encoder -> Parent Document Resolution."""
        # Step 1: Query both modalities
        dense_results = self._dense_search(query, top_k=top_k_candidates)
        sparse_results = self._sparse_search(query, top_k=top_k_candidates)

        # Step 2: Reciprocal Rank Fusion
        candidate_ids = self._reciprocal_rank_fusion(
            dense_results, sparse_results, top_k=top_k_candidates
        )
        if not candidate_ids:
            return []

        # Step 3: Build query-document pairs for Cross-Encoder scoring
        pairs = []
        candidate_meta = []
        for doc_id in candidate_ids:
            idx = self.id_to_idx[doc_id]
            text = self.documents[idx]
            meta = self.metadatas[idx]
            pairs.append((query, text))
            candidate_meta.append(meta)

        # Step 4: Cross-Encoder Reranking
        scores = self.reranker.predict(pairs)
        scored_candidates = sorted(
            zip(scores, candidate_meta), key=lambda x: x[0], reverse=True
        )

        # Step 5: Parent Document Deduplication
        seen_parents = set()
        citations = []

        for score, meta in scored_candidates:
            parent_id = meta["parent_id"]
            if parent_id in seen_parents:
                continue
            seen_parents.add(parent_id)

            parent_text = self.parent_store.get(
                parent_id, meta.get("parent_content", "")
            )

            citations.append(
                {
                    "policy_code": meta["policy_code"],
                    "policy_name": meta["policy_name"],
                    "section_title": meta["section_title"],
                    "parent_id": parent_id,
                    "clause_tags": [
                        tag for tag in meta["clause_tags"].split(",") if tag
                    ],
                    "content": parent_text,
                    "rerank_score": float(score),
                }
            )

            if len(citations) == final_top_k:
                break

        return citations