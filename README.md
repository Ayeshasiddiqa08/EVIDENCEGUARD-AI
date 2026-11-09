# 🛡️ EvidenceGuard AI
## NBA Accreditation Faculty Assistance Agent (RAG-Based)

> **IBM AICTE Agentic AI Project** | NBA May 2026 Edition / GAPC v4.0

---

## 📌 What is EvidenceGuard AI?

EvidenceGuard AI is a **Retrieval-Augmented Generation (RAG)**-based AI agent that helps engineering college faculty and NBA coordinators:

- Understand **NBA accreditation criteria** in simple language
- Identify **required documents** for each of the 10 NBA criteria
- Prepare and review **SAR (Self-Assessment Report)** evidence
- Calculate **CO-PO attainment** using the GAPC v4.0 formula
- Avoid **common accreditation errors** and missing documentation
- Navigate **Tier-I (Autonomous) and Tier-II (Affiliated)** differences

All answers are grounded in the official **EvidenceGuard AI NBA Knowledge Base (May 2026 Edition / GAPC v4.0)** — no fabricated requirements.

---

## 🗂️ Project Structure

```
EVIDENCEGUARD-AI/
│
├── backend/
│   ├── app.py                  ← Flask REST API (main server)
│   ├── rag_engine.py           ← RAG pipeline (TF-IDF retrieval + response synthesis)
│   ├── guardrails.py           ← Safety, accuracy, and scope enforcement
│   └── ibm_granite_engine.py   ← IBM Granite / watsonx.ai LLM integration
│
├── knowledge_base/
│   └── nba_knowledge_base.py   ← 26+ NBA knowledge chunks from the PDF
│
├── frontend/
│   └── index.html              ← Single-page web UI (chat + criteria table + evidence review)
│
├── docs/
│   ├── ARCHITECTURE.md         ← System architecture documentation
│   └── IBM_CLOUD_SETUP.md      ← Step-by-step IBM Cloud & Granite setup guide
│
├── evidenceguard.eve           ← Agent configuration file (RAG + IBM Granite settings)
├── guardrails_config.yaml      ← Complete guardrails specification (15 rules)
├── test_agent.py               ← Agent test suite (all required test questions)
├── requirements.txt            ← Python dependencies
├── run.bat                     ← One-click Windows launcher (auto-installs dependencies)
└── README.md                   ← This file
```

---

## ⚡ Quick Start (Windows)

### Step 1: Check Python is installed

Open **Command Prompt** or **PowerShell** and run:

```
python --version
```

You should see `Python 3.9` or higher. If not, download Python from https://www.python.org/downloads/

### Step 2: Install dependencies

Open a terminal in the `EVIDENCEGUARD-AI` folder and run:

```
pip install -r requirements.txt
```

This installs:
- `flask` — the web server
- `flask-cors` — allows the browser to talk to the server

> **No other dependencies needed.** The RAG engine uses only Python's built-in `math` and `re` modules.

### Step 3: Start the server

**Option A – Double-click** the `run.bat` file.

**Option B – Run manually** in terminal:

```
cd EVIDENCEGUARD-AI
python backend/app.py
```

You will see:

```
============================================================
  EvidenceGuard AI – NBA Accreditation Faculty Agent
  Running on http://127.0.0.1:5000
  Knowledge Base: NBA May 2026 Edition / GAPC v4.0
============================================================
```

### Step 4: Open the application

Open your web browser and go to:

```
http://127.0.0.1:5000
```

The EvidenceGuard AI chat interface will load automatically.

---

## 🖥️ How to Use

### Chat Tab (💬)
- Type any NBA accreditation question in the chat box.
- Press **Enter** to send (Shift+Enter for new line).
- Click any **quick question chip** on the welcome screen to try sample questions.
- Every answer shows **source references** and **relevant criteria**.

### Evidence Review Tab (📋)
1. Select an NBA criterion from the dropdown.
2. Optionally, enter the names of documents you have already prepared (press Enter after each).
3. Click **Review Evidence Requirements**.
4. The agent shows required evidence and common audit mistakes.

### Criteria Table Tab (📊)
- View all 10 NBA criteria with marks for both Tier-I and Tier-II.
- Click **Ask** on any row to get detailed guidance.

---

## 🔌 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Serves the frontend HTML |
| GET | `/api/health` | Server health check |
| POST | `/api/query` | Main RAG chat query |
| GET | `/api/criteria` | All 10 NBA criteria with marks |
| GET | `/api/quick-questions` | Sample faculty questions |
| POST | `/api/evidence-review` | Criterion-specific evidence guidance |

### Example: Query API

```bash
curl -X POST http://127.0.0.1:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What documents are needed for Criterion 5?"}'
```

Response:
```json
{
  "success": true,
  "query": "What documents are needed for Criterion 5?",
  "answer": "**Criterion 5 – Faculty Information...**",
  "sources": ["Section 5 – Criterion 5 Evidence | EvidenceGuard AI Knowledge Base"],
  "criteria": ["Criterion 5"],
  "confidence": "high",
  "retrieved_count": 3
}
```

---

## 🛡️ Guardrails

EvidenceGuard AI enforces mandatory guardrails:

| Guardrail | Description |
|-----------|-------------|
| **Out-of-scope blocking** | Rejects non-NBA topics (cricket, finance, etc.) |
| **Confidentiality protection** | Blocks queries with personal/financial data |
| **Anti-fabrication** | Refuses to make up criteria, marks, or requirements |
| **Compliance-claim prevention** | Never certifies a college as NBA-compliant |
| **Low-confidence notices** | Clearly states when information is not in the knowledge base |
| **Tier clarification** | Asks for Tier-I/II if question requires differentiation |
| **Input length validation** | Rejects empty or excessively long queries |

---

## 🧠 How the RAG Engine Works

```
Faculty Question
      │
      ▼
Input Guardrails (scope, confidentiality, fabrication check)
      │
      ▼
TF-IDF Tokenization of query
      │
      ▼
Cosine Similarity against 25+ pre-indexed NBA knowledge chunks
      │
      ▼
Top-3 most relevant chunks retrieved
      │
      ▼
Response synthesized from retrieved chunk content
      │
      ▼
Output Guardrails (low-confidence notice, compliance disclaimer)
      │
      ▼
Structured JSON response with sources and criteria
```

**No external LLM API required.** The RAG engine runs fully on-device using standard Python.

---

## 📚 Knowledge Base Coverage

| Section | Topics |
|---------|--------|
| Section 1 | NBA overview, objectives, benefits, NBA vs NAAC |
| Section 2 | Tier-I vs Tier-II, eligibility, 4-phase accreditation process |
| Section 3 | All 10 criteria with Tier-I and Tier-II marks |
| Section 4 | Complete documentation checklist (academic, faculty, lab) |
| Section 5 | Criterion-wise evidence mapping and common audit mistakes |
| Section 6 | SAR authoring workflow and consistency rules |
| Section 7 | GAPC v4.0 — 11 POs, CO-PO mapping scale, attainment formula |
| Section 8 | Internal audit workflow and compliance protocols |
| Section 9 | Common accreditation errors and prevention |
| Section 10 | Glossary of NBA terminology |
| Section 11 | 25 practical faculty FAQs with grounded answers |

---

## ⚠️ Important Disclaimer

EvidenceGuard AI is an **assistance tool** and **not an official NBA body**.

- Answers are grounded in the EvidenceGuard AI NBA Knowledge Base (May 2026 Edition).
- Always verify requirements against the **official NBA SAR manual** at https://www.nbaind.org/
- The agent will **never** claim that your institution is NBA-compliant or accredited.
- Only the official **NBA Peer Team and EAC** can determine accreditation status.

---

## 🏗️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.8+ / Flask 3.0 |
| IBM Granite LLM | `ibm/granite-13b-instruct-v2` via IBM watsonx.ai |
| IBM Cloud | IBM Cloud Lite (free) + IBM watsonx.ai |
| RAG Engine | TF-IDF + Cosine Similarity (built-in Python, no API needed) |
| Knowledge Base | 26+ chunked NBA knowledge documents (PDF-sourced) |
| Frontend | Vanilla HTML5 + CSS3 + JavaScript |
| Guardrails | Custom Python rules engine (15 enforced rules) |
| Agent Config | `evidenceguard.eve` (YAML-based agent configuration) |
| Deployment | Local (http://127.0.0.1:5000) |

> **IBM Technology is mandatory.** EvidenceGuard AI integrates IBM Granite
> via IBM watsonx.ai. When credentials are not set, the system falls back
> automatically to local TF-IDF mode. See `docs/IBM_CLOUD_SETUP.md` for setup.

---

## 📞 Project Info

- **Project:** IBM AICTE Agentic AI Internship
- **Agent Name:** EvidenceGuard AI
- **Target:** NBA Accreditation Faculty Assistance
- **Knowledge Base:** EvidenceGuard AI NBA Knowledge Base (May 2026 Edition / GAPC v4.0)
