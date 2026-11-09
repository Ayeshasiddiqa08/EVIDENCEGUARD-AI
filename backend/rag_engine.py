"""
EvidenceGuard AI – RAG Engine
Retrieval-Augmented Generation using TF-IDF + cosine similarity.
No external API required for retrieval. Language model response is
generated locally using template-based synthesis of retrieved chunks.
"""

from __future__ import annotations

import math
import re
import sys
import os

# Allow import from knowledge_base directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from knowledge_base.nba_knowledge_base import NBA_CHUNKS


# ---------------------------------------------------------------------------
# Text Preprocessing
# ---------------------------------------------------------------------------

STOP_WORDS = {
    "a", "an", "the", "is", "it", "in", "on", "of", "for", "to", "and",
    "or", "but", "with", "this", "that", "are", "was", "be", "as", "at",
    "by", "from", "do", "does", "what", "how", "which", "can", "i", "me",
    "my", "we", "you", "he", "she", "they", "us", "our", "your", "its",
    "have", "has", "had", "not", "no", "if", "then", "so", "about", "than",
    "should", "would", "could", "will", "need", "want", "tell", "give",
    "please", "explain", "describe", "list", "show"
}


def tokenize(text: str) -> list:
    """Lowercase, strip punctuation, remove stop words."""
    tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


# ---------------------------------------------------------------------------
# TF-IDF Vector Store (built once at import time)
# ---------------------------------------------------------------------------

class TFIDFVectorStore:
    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        self.doc_tokens = [tokenize(c["title"] + " " + c["content"]) for c in chunks]
        self.vocab = self._build_vocab()
        self.idf = self._compute_idf()
        self.tfidf_matrix = [self._tfidf(tokens) for tokens in self.doc_tokens]

    def _build_vocab(self) -> list[str]:
        vocab_set = set()
        for tokens in self.doc_tokens:
            vocab_set.update(tokens)
        return sorted(vocab_set)

    def _compute_idf(self) -> dict:
        N = len(self.doc_tokens)
        idf = {}
        for term in self.vocab:
            df = sum(1 for tokens in self.doc_tokens if term in tokens)
            idf[term] = math.log((N + 1) / (df + 1)) + 1  # smoothed IDF
        return idf

    def _tf(self, tokens: list[str]) -> dict:
        tf = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
        total = max(len(tokens), 1)
        return {t: count / total for t, count in tf.items()}

    def _tfidf(self, tokens: list[str]) -> dict:
        tf = self._tf(tokens)
        return {t: tf.get(t, 0) * self.idf.get(t, 0) for t in self.vocab}

    def _cosine_similarity(self, vec_a: dict, vec_b: dict) -> float:
        dot = sum(vec_a[t] * vec_b[t] for t in self.vocab)
        norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
        norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def retrieve(self, query: str, top_k: int = 3, min_score: float = 0.01) -> list[dict]:
        query_tokens = tokenize(query)
        query_vec = self._tfidf(query_tokens)
        scores = [
            (i, self._cosine_similarity(query_vec, doc_vec))
            for i, doc_vec in enumerate(self.tfidf_matrix)
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in scores[:top_k]:
            if score >= min_score:
                results.append({**self.chunks[idx], "relevance_score": round(score, 4)})
        return results


# Build the vector store once when module loads
_vector_store = TFIDFVectorStore(NBA_CHUNKS)


# ---------------------------------------------------------------------------
# Response Generator
# ---------------------------------------------------------------------------

def _format_answer(query: str, retrieved: list[dict]) -> dict:
    """
    Synthesize a structured answer from retrieved chunks with rich citations.

    Each retrieved chunk is numbered [1], [2], [3] … inline in the answer body.
    The sources list carries full citation strings including chunk ID and score.
    Returns a dict with: answer, sources, criteria, confidence, retrieved_count.
    """
    if not retrieved:
        return {
            "answer": (
                "ℹ️ **Information Not Found in Knowledge Base**\n\n"
                "I was unable to find relevant information in the NBA Knowledge Base "
                "to answer your question. This may mean:\n"
                "- The topic is not covered in the current knowledge base.\n"
                "- Try rephrasing with NBA-specific terms (e.g., SAR, CO-PO, SFR, Criterion 5).\n"
                "- For official details, consult: https://www.nbaind.org/\n\n"
                "**Suggested topics:** NBA criteria, SAR documents, CO-PO mapping, "
                "SFR, FDP requirements, Tier-I vs Tier-II, ATR, accreditation process."
            ),
            "sources": [],
            "criteria": [],
            "confidence": "low",
            "retrieved_count": 0,
        }

    sections      = []
    sources       = []
    rich_sources  = []          # detailed citations with ID and score
    criteria_set  = set()

    for ref_num, chunk in enumerate(retrieved, start=1):
        score  = chunk.get("relevance_score", 0.0)
        conf   = "HIGH" if score > 0.10 else "MED" if score > 0.03 else "LOW"
        cid    = chunk.get("id", f"chunk_{ref_num}")
        title  = chunk.get("title", "Untitled")
        source = chunk.get("source", "EvidenceGuard AI NBA Knowledge Base")

        # Section body with inline reference number
        sections.append(
            f"## [{ref_num}] {title}\n"
            f"{chunk['content']}"
        )

        # Plain source for backward compat (deduplicated later)
        sources.append(source)

        # Rich citation: "Section X.Y – Title | KB (chunk_id, score=0.24, HIGH)"
        rich_sources.append(
            f"[{ref_num}] {source}  "
            f"(id: {cid} | relevance: {score:.3f} | {conf})"
        )

        crit = chunk.get("criteria", "")
        if crit and crit not in ("General", "General – SAR", "General – Audit"):
            criteria_set.add(crit)

    answer_body = "\n\n---\n\n".join(sections)

    confidence = (
        "high"   if retrieved[0].get("relevance_score", 0) > 0.10 else
        "medium" if retrieved[0].get("relevance_score", 0) > 0.03 else
        "low"
    )

    disclaimer = (
        "\n\n---\n\n"
        "> 📚 **Sources & Citations:** "
        + " | ".join(
            f"[{i+1}] {c.get('source', '')}"
            for i, c in enumerate(retrieved)
        )
        + "\n\n"
        "> ⚠️ **Disclaimer:** This answer is grounded in the EvidenceGuard AI NBA Knowledge Base "
        "(May 2026 Edition / GAPC v4.0). Always verify requirements against the official NBA SAR "
        "manual at **https://www.nbaind.org/** before submitting any documents to NBA."
    )

    return {
        "answer":          answer_body + disclaimer,
        "sources":         list(dict.fromkeys(sources)),   # plain sources (deduped)
        "rich_sources":    rich_sources,                   # detailed citations
        "criteria":        sorted(criteria_set),
        "confidence":      confidence,
        "retrieved_count": len(retrieved),
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def query_knowledge_base(question: str, top_k: int = 3) -> dict:
    """
    Main RAG query function.
    Args:
        question: Natural-language question from faculty member.
        top_k: Number of chunks to retrieve (default 3).
    Returns:
        dict with keys: answer, sources, criteria, confidence, retrieved_count, _chunks.
        _chunks carries the raw retrieved dicts for optional IBM Granite augmentation.
    """
    retrieved = _vector_store.retrieve(question, top_k=top_k)
    result = _format_answer(question, retrieved)
    result["query"] = question
    result["_chunks"] = retrieved   # exposed for IBM Granite engine; not sent to frontend
    return result


def get_all_criteria_summary() -> list[dict]:
    """Return a brief summary of all 10 NBA criteria for the sidebar."""
    criteria_chunks = [c for c in NBA_CHUNKS if c["id"] == "criteria_overview"]
    if criteria_chunks:
        return criteria_chunks[0]
    return {}


def get_chunk_by_criteria(criteria_keyword: str) -> list[dict]:
    """Return all chunks matching a specific criterion keyword."""
    kw = criteria_keyword.lower()
    return [c for c in NBA_CHUNKS if kw in c.get("criteria", "").lower()]
