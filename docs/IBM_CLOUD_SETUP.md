# 🔧 IBM Cloud & IBM Granite Setup Guide
## EvidenceGuard AI – IBM Technology Integration

> **IBM Cloud Lite** and **IBM Granite** are mandatory for this project.
> Follow these steps to connect EvidenceGuard AI to IBM's AI services.

---

## What You Will Connect

| Service | Plan | Purpose |
|---------|------|---------|
| IBM Cloud Account | **Lite (Free)** | Access to all IBM services |
| IBM watsonx.ai | **Lite (Free)** | Host IBM Granite foundation model |
| IBM Granite Model | `ibm/granite-13b-instruct-v2` | LLM-enhanced NBA answers |

---

## Step 1 – Create a Free IBM Cloud Account

1. Go to **https://cloud.ibm.com/registration**
2. Fill in your email, name, and create a password.
3. Choose **Lite (Free)** plan — no credit card required.
4. Verify your email address.
5. Log in at **https://cloud.ibm.com**

---

## Step 2 – Provision IBM watsonx.ai (Lite Plan)

1. From the IBM Cloud dashboard, click **"Catalog"** in the top menu.
2. Search for **"Watson Machine Learning"**.
3. Click on **Watson Machine Learning** (by IBM).
4. Select the **Lite** plan (free).
5. Choose a region: **Dallas (us-south)** is recommended.
6. Click **"Create"**.
7. Wait 1–2 minutes for provisioning to complete.

---

## Step 3 – Create a watsonx.ai Project

1. Go to **https://dataplatform.cloud.ibm.com/wx**
2. Log in with your IBM Cloud credentials.
3. Click **"New Project"** → **"Create an empty project"**.
4. Name it: `EvidenceGuard-AI`
5. Click **"Create"**.
6. Once created, click on your project.
7. Click on the **"Manage"** tab in the project.
8. Copy the **Project ID** (it looks like: `abc12345-xxxx-xxxx-xxxx-xxxxxxxxxxxx`).
9. Save this — you will need it as `WATSONX_PROJECT_ID`.

---

## Step 4 – Generate an IBM Cloud API Key

1. Go to **https://cloud.ibm.com/iam/apikeys**
2. Click **"Create an IBM Cloud API key"**.
3. Name it: `EvidenceGuard-AI-Key`
4. Click **"Create"**.
5. **IMPORTANT:** Click **"Copy"** or **"Download"** immediately — the key is only shown once.
6. Save this — you will need it as `IBM_CLOUD_API_KEY`.

---

## Step 5 – Set Environment Variables

Open a **Command Prompt** or **PowerShell** window and run:

```bat
set IBM_CLOUD_API_KEY=your-api-key-here
set WATSONX_PROJECT_ID=your-project-id-here
set WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

> **Tip:** To make these permanent, go to Windows Settings →
> System → Advanced system settings → Environment Variables.

---

## Step 6 – Install the IBM watsonx.ai Python SDK

```bat
pip install ibm-watsonx-ai
```

---

## Step 7 – Update the Agent Configuration

Open `evidenceguard.eve` and change this line:

```yaml
  - id: "granite_llm"
    ...
    enabled: false   ← change this to true
```

Change it to:

```yaml
  - id: "granite_llm"
    ...
    enabled: true
```

---

## Step 8 – Test the Connection

Start the server (double-click `run.bat`), then open your browser and visit:

```
http://127.0.0.1:5000/api/health
```

You should see:

```json
{
  "status": "ok",
  "ibm_granite": {
    "connected": true,
    "model_id": "ibm/granite-13b-instruct-v2"
  }
}
```

If `connected` is `true`, **IBM Granite is active** and will generate enhanced answers.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `sdk_installed: false` | Run `pip install ibm-watsonx-ai` |
| `credentials_set: false` | Set `IBM_CLOUD_API_KEY` and `WATSONX_PROJECT_ID` env vars |
| `connected: false` | Check API key and project ID are correct; verify region URL |
| `401 Unauthorized` | Your API key may have expired — generate a new one |
| `404 Not Found` | Check `WATSONX_URL` matches your region (us-south, eu-gb, etc.) |

---

## Running Without IBM Credentials (Local Mode)

**You do not need IBM credentials to run EvidenceGuard AI.**

If credentials are not set, the system automatically uses the **local TF-IDF RAG engine** which:
- Requires no internet connection after install
- Works entirely on your computer
- Provides full NBA knowledge base access
- Just does not use IBM Granite for language generation

The `/api/health` endpoint will show `"rag_mode": "tfidf_local"` in this case.

---

## IBM Granite Models Available on watsonx.ai Lite

| Model ID | Size | Best For |
|----------|------|----------|
| `ibm/granite-3-8b-instruct` | 8B | Fast chat responses |
| `ibm/granite-13b-instruct-v2` | 13B | **Recommended** – balanced accuracy |
| `ibm/granite-3-2b-instruct` | 2B | Lightweight / demo |

To change the model, set:
```bat
set GRANITE_MODEL_ID=ibm/granite-3-8b-instruct
```

---

## IBM Cloud Lite Limits

| Resource | Lite Plan Limit |
|----------|----------------|
| watsonx.ai API calls | 500 per month |
| Tokens per call | 4096 |
| Storage | 5 GB |
| Projects | Unlimited |

For a demo or class project, the Lite plan is sufficient.

---

*Guide compiled for IBM AICTE Agentic AI Internship – EvidenceGuard AI*
