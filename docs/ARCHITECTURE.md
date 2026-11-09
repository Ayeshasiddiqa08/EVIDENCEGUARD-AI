# EvidenceGuard AI – System Architecture

## Overview

EvidenceGuard AI is a fully self-contained RAG-based faculty assistance agent
for NBA accreditation. It runs locally with no external API dependencies.

---

## Architecture Diagram (ASCII)

```
┌─────────────────────────────────────────────────────────────────┐
│                    FACULTY / USER (Browser)                     │
│              http://127.0.0.1:5000 (HTML/JS SPA)               │
└────────────────────────────┬────────────────────────────────────┘
                             │  HTTP REST (JSON)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              FLASK BACKEND  (backend/app.py)                    │
│                                                                 │
│  POST /api/query          GET /api/criteria                     │
│  POST /api/evidence-review GET /api/quick-questions             │
│  GET  /api/health          GET  /  (serves frontend)            │
└────────────┬────────────────────────────────┬───────────────────┘
             │                                │
             ▼                                ▼
┌────────────────────────┐      ┌─────────────────────────────┐
│   GUARDRAILS MODULE    │      │       RAG ENGINE             │
│  (backend/guardrails)  │      │   (backend/rag_engine.py)    │
│                        │      │                              │
│  • Input validation    │      │  1. Tokenize query           │
│  • Out-of-scope check  │      │  2. Compute TF-IDF vector    │
│  • Confidentiality     │      │  3. Cosine similarity search │
│  • Anti-fabrication    │      │  4. Retrieve top-K chunks    │
│  • Compliance claim    │      │  5. Synthesize response      │
│  • Tier clarification  │      │                              │
│  • Low-confidence flag │      │  ┌───────────────────────┐  │
└────────────────────────┘      │  │  TF-IDF VECTOR STORE  │  │
                                │  │  (built at startup)   │  │
                                │  │                       │  │
                                │  │  25+ NBA chunks       │  │
                                │  │  Vocabulary: ~800 terms│  │
                                │  │  IDF pre-computed     │  │
                                │  └───────────┬───────────┘  │
                                └──────────────┼──────────────┘
                                               │ reads from
                                               ▼
                             ┌─────────────────────────────────┐
                             │  KNOWLEDGE BASE MODULE          │
                             │  (knowledge_base/               │
                             │   nba_knowledge_base.py)        │
                             │                                 │
                             │  Source: NBA May 2026 Edition   │
                             │  GAPC v4.0 / Washington Accord  │
                             │                                 │
                             │  Sections covered:              │
                             │  1  NBA Introduction            │
                             │  2  Tier-I vs Tier-II           │
                             │  3  10 Criteria (1000 marks)    │
                             │  4  Documentation Checklist     │
                             │  5  Evidence Mapping            │
                             │  6  SAR Preparation Guide       │
                             │  7  CO-PO Mapping & Attainment  │
                             │  8  Internal Audit Protocols    │
                             │  9  Common Errors               │
                             │  10 Glossary                    │
                             │  11 25 Faculty FAQs             │
                             └─────────────────────────────────┘
```

---

## Component Descriptions

### 1. Frontend (`frontend/index.html`)
- Single-page application built with vanilla HTML5, CSS3, and JavaScript
- Three panels: Chat, Evidence Review, Criteria Table
- Communicates with backend via `fetch()` REST calls
- No external JavaScript frameworks or CDN dependencies
- Renders markdown-like formatting for structured answers

### 2. Flask Backend (`backend/app.py`)
- Python Flask 3.0 REST API server
- Serves both the frontend HTML and the API endpoints
- CORS enabled for browser compatibility
- Handles input validation, routes to guardrails and RAG engine
- Assembles structured JSON response with answer, sources, criteria, confidence

### 3. RAG Engine (`backend/rag_engine.py`)
- **Chunking**: 25+ pre-chunked knowledge documents with section, title, content, source, and criteria metadata
- **Indexing**: TF-IDF vectorization at startup — vocabulary built from all chunks, IDF pre-computed
- **Retrieval**: Cosine similarity between query vector and all document vectors, top-K returned
- **Response Synthesis**: Chunk titles and content assembled into structured markdown answer with disclaimer
- **No external dependency**: Pure Python `math` and `re` — no NumPy, no OpenAI, no IBM watsonx API required

### 4. Guardrails (`backend/guardrails.py`)
- **Input guardrails** (run before retrieval):
  - `validate_query_length` — rejects empty, too short, or too long queries
  - `check_out_of_scope` — blocks non-NBA topics
  - `check_confidential` — blocks personal/financial data exposure
  - `check_fabrication_request` — blocks jailbreak/bypass attempts
  - `check_compliance_claim` — adds disclaimer when compliance is implied
  - `check_tier_missing` — requests Tier-I/II clarification when relevant
- **Output guardrails** (run after retrieval):
  - `check_low_confidence_answer` — replaces empty answers with informative not-found message

### 5. Knowledge Base (`knowledge_base/nba_knowledge_base.py`)
- 25+ structured knowledge chunks extracted from the NBA Knowledge Base PDF
- Each chunk contains: `id`, `section`, `title`, `content`, `source`, `criteria`
- Grounded exclusively in the official NBA SAR manual (May 2026 / GAPC v4.0)
- Covers all 10 NBA criteria, CO-PO mapping, SAR preparation, audit protocols, and FAQs

---

## Data Flow: Chat Query

```
1. User submits question via browser
2. Frontend sends POST /api/query with { question, top_k }
3. Backend validates query length
4. Input guardrails run:
   a. Out-of-scope check → block if non-NBA
   b. Confidentiality check → block if personal data
   c. Fabrication check → block if jailbreak attempt
   d. Compliance claim check → add warning if compliance claim
   e. Tier clarification check → add notice if tier-specific and unspecified
5. RAG engine retrieves top-3 chunks by cosine similarity
6. Response synthesized from chunk titles and content
7. Output guardrail adds not-found notice if confidence is very low
8. JSON response returned: { answer, sources, criteria, confidence, retrieved_count }
9. Frontend renders answer with markdown formatting, source pills, confidence badge
```

---

## NBA Knowledge Base Coverage Statistics

| Metric | Value |
|--------|-------|
| Total knowledge chunks | 25+ |
| Criteria covered | All 10 (Criterion 1 through 10) |
| FAQs indexed | 11 directly + 14 referenced |
| NBA Manual version | May 2026 Edition |
| OBE Framework | GAPC v4.0 (Washington Accord 2021) |
| Target institutions | Tier-I (Autonomous) and Tier-II (Affiliated) |
| Program scope | UG Engineering and Technical Programmes |

---

## Guardrails Coverage

| Guardrail Type | Rule | Action |
|----------------|------|--------|
| Input | Empty / too-short query | Block with guidance |
| Input | Non-NBA topic (sports, finance, etc.) | Block with out-of-scope message |
| Input | Personal/financial data in query | Block with privacy notice |
| Input | Jailbreak / fabrication request | Block with refusal |
| Input | Compliance certification request | Allow with mandatory disclaimer |
| Input | Tier-specific but tier unspecified | Allow with clarification prompt |
| Output | Zero retrieval results | Replace with not-found guidance |
| Output | Low similarity score | Add low-confidence notice |

---

## Security and Privacy Notes

- No user data is stored or logged persistently
- No external API calls are made
- All processing happens on-device (localhost only)
- The knowledge base contains only official public NBA documentation

---

## References

1. National Board of Accreditation (NBA), General Manual of Accreditation for UG Engineering Programmes (Tier-I & Tier-II), May 2026 Edition, New Delhi. https://www.nbaind.org/
2. International Engineering Alliance (IEA), Graduate Attributes and Professional Competencies Framework v4.0 (WA 2021 Alignment), June 2021.
3. NBA eNBA Portal Manual, Pre-Qualifier Guidelines & SAR Format for Tier-I and Tier-II Institutions.
4. AICTE Approval Process Handbook (APH), Statutory Norms for Technical Institutions.
