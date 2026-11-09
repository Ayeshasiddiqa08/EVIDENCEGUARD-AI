"""
EvidenceGuard AI – Flask Backend API
Provides REST endpoints for the RAG-based NBA faculty assistance agent.

IBM Technology:
  - IBM Cloud Lite (free tier)
  - IBM watsonx.ai
  - IBM Granite foundation model (ibm/granite-13b-instruct-v2)

The IBM Granite engine is optional.  If credentials are not configured
the system falls back automatically to local TF-IDF RAG synthesis.
"""

import os
import sys
import json
import traceback
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ── path setup ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, BASE_DIR)

from rag_engine import query_knowledge_base, get_all_criteria_summary, _vector_store
from guardrails import (
    run_input_guardrails,
    run_output_guardrails,
    validate_query_length,
)

# IBM Granite engine (graceful fallback if not configured)
try:
    from ibm_granite_engine import generate_response as granite_generate, check_granite_connection
    GRANITE_AVAILABLE = True
except ImportError:
    GRANITE_AVAILABLE = False
    def granite_generate(*args, **kwargs):
        return {"answer": None, "model": "tfidf_local", "fallback": True, "sources": []}
    def check_granite_connection():
        return {"sdk_installed": False, "connected": False, "error": "Module not found"}

# ── app setup ────────────────────────────────────────────────────────────────
app = Flask(
    __name__,
    static_folder=os.path.join(ROOT_DIR, "frontend"),
    static_url_path="",
)
CORS(app)  # allow cross-origin requests from the frontend


# ── helpers ──────────────────────────────────────────────────────────────────

def _error_response(message: str, status: int = 400) -> tuple:
    return jsonify({"success": False, "error": message}), status


def _build_full_response(query: str, rag_result: dict, warnings: list, clarifications: list) -> dict:
    """Assemble the final JSON payload sent to the frontend."""
    answer_parts = []

    # Prepend clarification notices (soft)
    if clarifications:
        answer_parts.extend(clarifications)

    # Prepend warnings (compliance disclaimer etc.)
    if warnings:
        answer_parts.extend(warnings)

    # Main answer
    answer_parts.append(rag_result["answer"])

    full_answer = "\n\n".join(answer_parts)

    return {
        "success":         True,
        "query":           query,
        "answer":          full_answer,
        "sources":         rag_result.get("sources", []),
        "rich_sources":    rag_result.get("rich_sources", []),
        "criteria":        rag_result.get("criteria", []),
        "confidence":      rag_result.get("confidence", "unknown"),
        "retrieved_count": rag_result.get("retrieved_count", 0),
        "model":           rag_result.get("model", "tfidf_local"),
        # _chunks is internal; never sent to frontend
    }


# ── routes ───────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def serve_index():
    """Serve the frontend HTML."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint – includes IBM Granite connection status."""
    granite_status = check_granite_connection()
    return jsonify({
        "status": "ok",
        "agent": "EvidenceGuard AI",
        "version": "1.0.0",
        "knowledge_base": "NBA May 2026 Edition (GAPC v4.0)",
        "rag_mode": "tfidf_local" if granite_status.get("fallback", True) else "ibm_granite",
        "ibm_granite": {
            "sdk_installed": granite_status.get("sdk_installed", False),
            "connected": granite_status.get("connected", False),
            "model_id": granite_status.get("model_id", "ibm/granite-13b-instruct-v2"),
            "watsonx_url": granite_status.get("watsonx_url", ""),
            "error": granite_status.get("error"),
        },
        "chunks_loaded": len(_vector_store.chunks),
        "ibm_technology": [
            "IBM Cloud Lite",
            "IBM watsonx.ai",
            "IBM Granite (ibm/granite-13b-instruct-v2)",
        ]
    })


@app.route("/api/query", methods=["POST"])
def handle_query():
    """
    Main RAG query endpoint.
    Request body: {"question": "...", "top_k": 3}
    Response:     {success, query, answer, sources, criteria, confidence, retrieved_count}
    """
    try:
        data = request.get_json(silent=True) or {}
        question = data.get("question", "").strip()
        top_k = min(int(data.get("top_k", 3)), 5)  # cap at 5

        # ── Step 1: Validate length ──────────────────────────────────────────
        length_check = validate_query_length(question)
        if not length_check["valid"]:
            return _error_response(length_check["message"])

        # ── Step 2: Input guardrails ─────────────────────────────────────────
        guard_result = run_input_guardrails(question)
        if not guard_result["pass"]:
            return jsonify({
                "success": False,
                "blocked": True,
                "query": question,
                "answer": guard_result["message"],
                "sources": [],
                "criteria": [],
                "confidence": "blocked",
                "retrieved_count": 0,
            })

        warnings = guard_result.get("warnings", [])
        clarifications = guard_result.get("clarifications", [])

        # ── Step 3: RAG Retrieval (TF-IDF) ──────────────────────────────────
        rag_result = query_knowledge_base(question, top_k=top_k)

        # ── Step 4: IBM Granite LLM Augmentation (if configured) ────────────
        granite_result = granite_generate(question, rag_result.get("_chunks", []))
        if granite_result.get("answer"):
            # Use IBM Granite generated answer, keep retrieval metadata
            rag_result["answer"] = granite_result["answer"]
            rag_result["model"] = granite_result["model"]
        else:
            rag_result["model"] = "tfidf_local"

        # ── Step 5: Output guardrails ────────────────────────────────────────
        rag_result = run_output_guardrails(rag_result)

        # ── Step 6: Build and return response ───────────────────────────────
        response = _build_full_response(question, rag_result, warnings, clarifications)
        return jsonify(response)

    except Exception as exc:
        traceback.print_exc()
        return _error_response(
            "An unexpected server error occurred. Please try again.", 500
        )


@app.route("/api/criteria", methods=["GET"])
def get_criteria():
    """Return overview of all 10 NBA criteria for the sidebar."""
    criteria_data = [
        {"id": 1,  "name": "Vision, Mission & PEOs",               "marks_t1": 50,  "marks_t2": 50},
        {"id": 2,  "name": "Curriculum & Teaching-Learning",        "marks_t1": 100, "marks_t2": 120},
        {"id": 3,  "name": "Course Outcomes (COs) & Program Outcomes (POs)", "marks_t1": 175, "marks_t2": 120},
        {"id": 4,  "name": "Students' Performance Evaluation",      "marks_t1": 100, "marks_t2": 150},
        {"id": 5,  "name": "Faculty Information & Contributions",   "marks_t1": 200, "marks_t2": 200},
        {"id": 6,  "name": "Facilities & Technical Support",        "marks_t1": 80,  "marks_t2": 80},
        {"id": 7,  "name": "Continuous Improvement (CQI)",          "marks_t1": 75,  "marks_t2": 50},
        {"id": 8,  "name": "First Year Academics (Institute)",      "marks_t1": 50,  "marks_t2": 50},
        {"id": 9,  "name": "Student Support Systems (Institute)",   "marks_t1": 50,  "marks_t2": 50},
        {"id": 10, "name": "Governance & Financial Resources",      "marks_t1": 120, "marks_t2": 120},
    ]
    return jsonify({"success": True, "criteria": criteria_data})


@app.route("/api/quick-questions", methods=["GET"])
def get_quick_questions():
    """Return sample questions for faculty to try."""
    questions = [
        "What documents are required for Criterion 5 (faculty)?",
        "How do I calculate CO attainment using the 80-20 formula?",
        "What is the SFR requirement for 6-year NBA accreditation?",
        "What are the 11 Program Outcomes under GAPC v4.0?",
        "What is the difference between Tier-I and Tier-II in NBA?",
        "What common errors should I avoid in the SAR?",
        "What is an Action Taken Report (ATR) and when is it needed?",
        "How many Ph.D. faculty are required for NBA accreditation?",
        "What documents should be in a course file for NBA?",
        "What is the CO-PO mapping scale used in NBA?",
        "Explain the NBA accreditation process step by step.",
        "What is the minimum FDP duration for faculty in NBA?",
    ]
    return jsonify({"success": True, "questions": questions})


@app.route("/api/retrieve", methods=["POST"])
def retrieve():
    """
    Explicit document retrieval endpoint.
    Shows exactly which knowledge-base chunks are matched for a query,
    including their relevance scores, section, criteria, and source.

    Request body: {"question": "...", "top_k": 5}
    Response:     {success, query, retrieved_count, chunks: [{id, title, section,
                   criteria, source, relevance_score, content_preview}]}
    """
    try:
        data = request.get_json(silent=True) or {}
        question = data.get("question", "").strip()
        top_k = min(int(data.get("top_k", 5)), 10)

        if not question:
            return _error_response("Please provide a question.")

        # Run guardrails first — respect the same rules as /api/query
        length_check = validate_query_length(question)
        if not length_check["valid"]:
            return _error_response(length_check["message"])

        guard = run_input_guardrails(question)
        if not guard["pass"]:
            return jsonify({
                "success": False,
                "blocked": True,
                "query": question,
                "reason": guard.get("message", "Blocked by guardrail"),
                "chunks": [],
                "retrieved_count": 0,
            })

        # Retrieve raw chunks
        from rag_engine import tokenize
        chunks = _vector_store.retrieve(question, top_k=top_k, min_score=0.001)

        serialised = []
        for c in chunks:
            serialised.append({
                "id":               c.get("id", ""),
                "title":            c.get("title", ""),
                "section":          c.get("section", ""),
                "criteria":         c.get("criteria", ""),
                "source":           c.get("source", ""),
                "relevance_score":  c.get("relevance_score", 0.0),
                "confidence_label": (
                    "high"   if c.get("relevance_score", 0) > 0.10 else
                    "medium" if c.get("relevance_score", 0) > 0.03 else
                    "low"
                ),
                "content_preview":  c.get("content", "")[:300] + (
                    "…" if len(c.get("content", "")) > 300 else ""
                ),
            })

        return jsonify({
            "success":        True,
            "query":          question,
            "retrieved_count": len(serialised),
            "query_tokens":   tokenize(question),
            "chunks":         serialised,
        })

    except Exception:
        traceback.print_exc()
        return _error_response("Retrieval error. Please try again.", 500)


@app.route("/api/kb-stats", methods=["GET"])
def kb_stats():
    """
    Knowledge base inspection endpoint.
    Returns a summary of all loaded chunks with their metadata —
    useful for verifying that the knowledge base is fully wired.
    """
    from knowledge_base.nba_knowledge_base import NBA_CHUNKS

    sections   = {}
    criteria_c = {}
    chunk_ids  = []

    for c in NBA_CHUNKS:
        sec = c.get("section", "Unknown")
        sections[sec] = sections.get(sec, 0) + 1

        crit = c.get("criteria", "General")
        criteria_c[crit] = criteria_c.get(crit, 0) + 1

        chunk_ids.append({
            "id":       c.get("id"),
            "title":    c.get("title"),
            "criteria": c.get("criteria"),
            "source":   c.get("source"),
        })

    return jsonify({
        "success":       True,
        "total_chunks":  len(NBA_CHUNKS),
        "vocab_size":    len(_vector_store.vocab),
        "sections":      sections,
        "criteria_dist": criteria_c,
        "chunks":        chunk_ids,
        "rag_engine":    "TF-IDF Cosine Similarity (built-in Python)",
        "kb_version":    "NBA May 2026 Edition / GAPC v4.0",
    })


@app.route("/api/evidence-review", methods=["POST"])
def evidence_review():
    """
    Evidence review helper.
    Request: {"criterion": "Criterion 5", "submitted_docs": ["...", "..."]}
    Response: guidance on what is missing based on knowledge base.
    """
    try:
        data = request.get_json(silent=True) or {}
        criterion = data.get("criterion", "").strip()
        submitted = data.get("submitted_docs", [])

        if not criterion:
            return _error_response("Please specify a criterion (e.g., 'Criterion 5').")

        # Build a query to check requirements for the criterion
        query = f"What documents are required for {criterion} and what are common mistakes?"
        rag_result = query_knowledge_base(query, top_k=3)
        rag_result = run_output_guardrails(rag_result)

        submitted_lower = [d.lower() for d in submitted]
        review_notes = []

        if submitted_lower:
            review_notes.append(
                f"✅ You have submitted **{len(submitted)}** document(s): "
                + ", ".join(f"`{d}`" for d in submitted[:5])
                + ("..." if len(submitted) > 5 else "")
            )
            review_notes.append(
                "⚠️ **Please compare your documents against the evidence requirements below.** "
                "EvidenceGuard AI cannot independently verify whether your specific documents "
                "are complete or compliant — only an NBA Peer Team can make that determination."
            )
        else:
            review_notes.append(
                "ℹ️ No specific documents were provided for review. "
                "Showing all required evidence for the selected criterion."
            )

        full_answer = "\n\n".join(review_notes) + "\n\n---\n\n" + rag_result["answer"]

        return jsonify({
            "success": True,
            "criterion": criterion,
            "answer": full_answer,
            "sources": rag_result.get("sources", []),
            "criteria": rag_result.get("criteria", []),
        })

    except Exception:
        traceback.print_exc()
        return _error_response("Evidence review error. Please try again.", 500)


# ── entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "true").lower() == "true"
    print(f"\n{'='*60}")
    print(f"  EvidenceGuard AI – NBA Accreditation Faculty Agent")
    print(f"  Running on http://127.0.0.1:{port}")
    print(f"  Knowledge Base: NBA May 2026 Edition / GAPC v4.0")
    print(f"{'='*60}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
