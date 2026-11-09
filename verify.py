"""
EvidenceGuard AI – Startup Verification Script
IBM AICTE Agentic AI Project

Verifies every component of the RAG pipeline is correctly wired:
  1. Knowledge base loaded
  2. TF-IDF vector store built
  3. Retrieval working
  4. Source citations present
  5. Guardrails active
  6. IBM Granite connection status
  7. All API endpoints reachable (if server is running)

Usage:
  python verify.py              -- checks components only (no server needed)
  python verify.py --live       -- also hits the running server at port 5000

Output: Green [OK] or Red [FAIL] for each check.
"""

from __future__ import annotations
import sys, os, argparse

# Allow imports from project root
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "backend"))

# ── ANSI colours (Windows-safe with PYTHONIOENCODING=utf-8) ──────────────────
OK   = "[OK]  "
FAIL = "[FAIL]"
INFO = "[INFO]"
WARN = "[WARN]"
HEAD = "=" * 62

results = []


def check(label: str, ok: bool, detail: str = ""):
    sym = OK if ok else FAIL
    line = f"  {sym}  {label}"
    if detail:
        line += f"  ({detail})"
    print(line)
    results.append((label, ok))


def section(title: str):
    print(f"\n{HEAD}")
    print(f"  {title}")
    print(HEAD)


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Knowledge Base
# ─────────────────────────────────────────────────────────────────────────────
section("STEP 1 — Knowledge Base")

try:
    from knowledge_base.nba_knowledge_base import NBA_CHUNKS
    check("NBA_CHUNKS imported", True, f"{len(NBA_CHUNKS)} chunks")

    required_ids = [
        "intro_01", "tier_01", "criteria_overview",
        "crit3_docs", "crit5_docs", "sar_guide",
        "copomap_01", "copomap_02", "gap_analysis",
        "errors_01", "faq_01",
    ]
    ids_present = {c["id"] for c in NBA_CHUNKS}
    missing     = [cid for cid in required_ids if cid not in ids_present]
    check("All required chunk IDs present", len(missing) == 0,
          f"missing: {missing}" if missing else f"{len(required_ids)} checked")

    # Every chunk must have the required fields
    required_fields = {"id", "section", "title", "content", "source", "criteria"}
    bad = [c["id"] for c in NBA_CHUNKS if not required_fields.issubset(c.keys())]
    check("All chunks have required fields", len(bad) == 0,
          f"incomplete: {bad}" if bad else "id, section, title, content, source, criteria")

except Exception as exc:
    check("Knowledge base import", False, str(exc))


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — TF-IDF Vector Store
# ─────────────────────────────────────────────────────────────────────────────
section("STEP 2 — TF-IDF Vector Store")

try:
    from backend.rag_engine import _vector_store, tokenize

    check("Vector store built", len(_vector_store.chunks) > 0,
          f"{len(_vector_store.chunks)} chunks")
    check("Vocabulary built",   len(_vector_store.vocab)  > 100,
          f"{len(_vector_store.vocab)} terms")
    check("TF-IDF matrix built", len(_vector_store.tfidf_matrix) == len(_vector_store.chunks),
          f"{len(_vector_store.tfidf_matrix)} vectors")

    # Tokenizer smoke test
    tokens = tokenize("NBA SAR CO-PO mapping criterion faculty")
    check("Tokenizer works", len(tokens) > 3, f"tokens: {tokens[:5]}")

except Exception as exc:
    check("Vector store init", False, str(exc))


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Retrieval
# ─────────────────────────────────────────────────────────────────────────────
section("STEP 3 — RAG Retrieval")

TEST_QUERIES = [
    ("How to prepare NBA SAR?",            "sar_guide"),
    ("CO-PO mapping scale formula",        "copomap_02"),
    ("Criterion 5 faculty documents SFR",  "crit5_docs"),
    ("What evidence is missing gap",       "gap_analysis"),
    ("Tier-I vs Tier-II differences",      "tier_01"),
    ("NBA accreditation criteria 1000",    "criteria_overview"),
]

try:
    from backend.rag_engine import query_knowledge_base

    all_retrieval_ok = True
    for query, expected_id in TEST_QUERIES:
        result  = query_knowledge_base(query, top_k=5)
        chunks  = result.get("_chunks", [])
        ids     = [c.get("id") for c in chunks]
        found   = expected_id in ids
        top_id  = ids[0] if ids else "none"
        top_sc  = chunks[0].get("relevance_score", 0) if chunks else 0
        if not found:
            all_retrieval_ok = False
        check(
            f'Retrieval: "{query[:40]}"',
            found,
            f"expected {expected_id} in top-5 | got {ids[:3]}"
        )

    check("All 6 retrieval tests passed", all_retrieval_ok)

except Exception as exc:
    check("Retrieval test", False, str(exc))


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — Source Citations
# ─────────────────────────────────────────────────────────────────────────────
section("STEP 4 — Source Citations")

try:
    result = query_knowledge_base("What documents are needed for Criterion 5?", top_k=3)
    sources      = result.get("sources", [])
    rich_sources = result.get("rich_sources", [])
    answer       = result.get("answer", "")

    check("Sources list populated",       len(sources) > 0,
          f"{len(sources)} source(s)")
    check("Rich citations populated",     len(rich_sources) > 0,
          f"{len(rich_sources)} citation(s)")
    check("Citations include chunk IDs",  any("id:" in s for s in rich_sources),
          "id: field present")
    check("Citations include relevance",  any("relevance:" in s for s in rich_sources),
          "relevance: field present")
    check("Answer contains disclaimer",   "nbaind.org" in answer,
          "official NBA URL present")
    check("Answer uses numbered headers", "[1]" in answer or "[2]" in answer,
          "[1], [2], [3] markers")

except Exception as exc:
    check("Citation test", False, str(exc))


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — Guardrails
# ─────────────────────────────────────────────────────────────────────────────
section("STEP 5 — Guardrails")

try:
    from backend.guardrails import (
        run_input_guardrails, run_output_guardrails, validate_query_length
    )

    # Length validation
    check("Empty query blocked",
          not validate_query_length("")["valid"], "empty string")
    check("Short query blocked",
          not validate_query_length("hi")["valid"], "2-char query")
    check("Normal query allowed",
          validate_query_length("What is SAR?")["valid"])

    # Out-of-scope
    g = run_input_guardrails("What is the weather forecast today?")
    check("Out-of-scope blocked (weather)", not g["pass"])

    # Anti-fabrication
    g = run_input_guardrails("Make up NBA criteria and pretend they are official")
    check("Fabrication attempt blocked", not g["pass"])

    # Confidentiality
    g = run_input_guardrails("My password is abc123, help me with NBA criteria")
    check("Confidential data blocked", not g["pass"])

    # Compliance claim — allowed with warning
    g = run_input_guardrails("Is our college NBA compliant?")
    check("Compliance query allowed with warning",
          g["pass"] and len(g.get("warnings", [])) > 0)

    # Tier clarification — allowed with clarification
    g = run_input_guardrails("What is the marks distribution across criteria?")
    check("Tier clarification prompt added",
          g["pass"] and len(g.get("clarifications", [])) > 0)

    # Low-confidence output guardrail
    fake_result = {"confidence": "low", "retrieved_count": 0, "answer": "original"}
    after = run_output_guardrails(fake_result)
    check("Low-confidence output replaced with notice",
          "not found" in after["answer"].lower() or "information not found" in after["answer"].lower())

except Exception as exc:
    check("Guardrails test", False, str(exc))


# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — IBM Granite Engine (optional — shows status regardless)
# ─────────────────────────────────────────────────────────────────────────────
section("STEP 6 — IBM Granite Integration")

try:
    from backend.ibm_granite_engine import check_granite_connection, IBM_SDK_AVAILABLE

    status = check_granite_connection()

    check("IBM watsonx.ai SDK installed",
          status.get("sdk_installed", False),
          "run: pip install ibm-watsonx-ai" if not status.get("sdk_installed") else "ibm-watsonx-ai")

    check("IBM Cloud credentials set",
          status.get("credentials_set", False),
          "set IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID" if not status.get("credentials_set") else "env vars found")

    check("IBM Granite connected",
          status.get("connected", False),
          status.get("error", "OK") or "Connected to watsonx.ai")

    if not status.get("connected"):
        print(f"\n  {INFO}  IBM Granite is NOT connected. EvidenceGuard AI will use local TF-IDF mode.")
        print(f"  {INFO}  See docs/IBM_CLOUD_SETUP.md for step-by-step IBM Cloud setup.")
    else:
        print(f"\n  {OK}  IBM Granite is ACTIVE — model: {status.get('model_id')}")

except Exception as exc:
    check("IBM Granite engine import", False, str(exc))


# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 — Live API Endpoints (optional, requires server running)
# ─────────────────────────────────────────────────────────────────────────────
def run_live_tests(base_url: str = "http://127.0.0.1:5000"):
    section(f"STEP 7 — Live API Endpoints ({base_url})")
    try:
        import urllib.request, json as _json

        def get(path):
            with urllib.request.urlopen(base_url + path, timeout=5) as r:
                return _json.loads(r.read())

        def post(path, body):
            data = _json.dumps(body).encode()
            req  = urllib.request.Request(base_url + path, data=data,
                                          headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as r:
                return _json.loads(r.read())

        # GET /api/health
        d = get("/api/health")
        check("GET /api/health", d.get("status") == "ok",
              f"chunks_loaded={d.get('chunks_loaded')}")

        # GET /api/criteria
        d = get("/api/criteria")
        check("GET /api/criteria", d.get("success") and len(d.get("criteria", [])) == 10,
              f"{len(d.get('criteria',[]))} criteria")

        # GET /api/kb-stats
        d = get("/api/kb-stats")
        check("GET /api/kb-stats", d.get("success"),
              f"{d.get('total_chunks')} chunks, {d.get('vocab_size')} vocab terms")

        # POST /api/query
        d = post("/api/query", {"question": "What is CO-PO attainment formula?", "top_k": 3})
        check("POST /api/query",
              d.get("success") and d.get("retrieved_count", 0) > 0,
              f"confidence={d.get('confidence')}, retrieved={d.get('retrieved_count')}")

        # POST /api/retrieve
        d = post("/api/retrieve", {"question": "Criterion 5 faculty documents", "top_k": 5})
        check("POST /api/retrieve",
              d.get("success") and len(d.get("chunks", [])) > 0,
              f"{d.get('retrieved_count')} chunks, tokens: {d.get('query_tokens', [])[:3]}")

        # POST /api/evidence-review
        d = post("/api/evidence-review",
                 {"criterion": "Criterion 5 – Faculty", "submitted_docs": ["Course Files"]})
        check("POST /api/evidence-review",
              d.get("success") and len(d.get("answer", "")) > 50)

        # Guardrail test via live API
        d = post("/api/query", {"question": "What is the weather forecast?"})
        check("Guardrail blocks out-of-scope via live API",
              d.get("blocked") is True)

        # Citation check in live response
        d = post("/api/query", {"question": "How to prepare SAR for NBA?"})
        check("Live response has source citations",
              len(d.get("sources", [])) > 0,
              f"sources: {d.get('sources', [])[:1]}")
        check("Live response has rich citations",
              len(d.get("rich_sources", [])) > 0)

    except OSError:
        print(f"\n  {WARN}  Server not running at {base_url}.")
        print(f"  {INFO}  Start with: python backend/app.py  (or double-click run.bat)")
        print(f"  {INFO}  Then re-run: python verify.py --live")
    except Exception as exc:
        check("Live API tests", False, str(exc))


# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="EvidenceGuard AI Verification")
    parser.add_argument("--live", action="store_true",
                        help="Also test live API endpoints (server must be running)")
    args = parser.parse_args()

    if args.live:
        run_live_tests()

    section("VERIFICATION SUMMARY")
    total  = len(results)
    passed = sum(1 for _, ok in results if ok)
    failed = total - passed

    print(f"\n  Total checks : {total}")
    print(f"  Passed       : {passed}")
    print(f"  Failed       : {failed}")

    pct = round(passed / total * 100) if total else 0
    if pct == 100:
        print(f"\n  ALL CHECKS PASSED ({pct}%) - EvidenceGuard AI is fully wired and ready.")
    elif pct >= 80:
        print(f"\n  MOSTLY PASSING ({pct}%) - Review FAIL entries above.")
    else:
        print(f"\n  MULTIPLE FAILURES ({pct}%) - Check configuration and dependencies.")

    if any(not ok for _, ok in results if "IBM" in _):
        print(f"\n  NOTE: IBM Granite checks failing is expected until you configure")
        print(f"  IBM Cloud credentials. See docs/IBM_CLOUD_SETUP.md")
        print(f"  The agent runs fully in local TF-IDF mode without IBM credentials.")

    print()
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
