"""
EvidenceGuard AI – IBM Granite / watsonx.ai Integration Engine
IBM AICTE Agentic AI Project

This module adds IBM Granite LLM augmentation on top of the existing
TF-IDF RAG retrieval engine.  It is optional: if IBM Cloud credentials
are not configured, the system falls back automatically to the
built-in TF-IDF template-based answer synthesis.

Mandatory IBM Technology:
  - IBM Cloud Lite (free tier)
  - IBM watsonx.ai
  - IBM Granite foundation model (ibm/granite-13b-instruct-v2)

Setup:
  1. Create a free IBM Cloud account at https://cloud.ibm.com/registration
  2. Provision IBM watsonx.ai (Lite plan) from IBM Cloud catalog
  3. Create a project in watsonx.ai and copy the Project ID
  4. Generate an IBM Cloud API key from IAM > API Keys
  5. Set these environment variables:
       IBM_CLOUD_API_KEY=<your-api-key>
       WATSONX_PROJECT_ID=<your-project-id>
       WATSONX_URL=https://us-south.ml.cloud.ibm.com  (or your region)
  6. In evidenceguard.eve, set tools.granite_llm.enabled = true
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

# ── IBM watsonx.ai SDK (ibm-watsonx-ai) ─────────────────────────────────────
# Install with: pip install ibm-watsonx-ai
# This import is optional – the module gracefully degrades if not installed.
try:
    from ibm_watsonx_ai import APIClient, Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    IBM_SDK_AVAILABLE = True
except ImportError:
    IBM_SDK_AVAILABLE = False
    logger.warning(
        "ibm-watsonx-ai SDK not installed. "
        "Run: pip install ibm-watsonx-ai\n"
        "EvidenceGuard AI will use the local TF-IDF engine instead."
    )


# ── Configuration ─────────────────────────────────────────────────────────────
IBM_CLOUD_API_KEY   = os.environ.get("IBM_CLOUD_API_KEY", "")
WATSONX_PROJECT_ID  = os.environ.get("WATSONX_PROJECT_ID", "")
WATSONX_URL         = os.environ.get("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

# IBM Granite model – preferred for factual, RAG-grounded tasks
GRANITE_MODEL_ID    = os.environ.get("GRANITE_MODEL_ID", "ibm/granite-13b-instruct-v2")

# Generation parameters (conservative for factual NBA guidance)
# Built lazily so the module loads even without the IBM SDK installed.
def _build_generation_params():
    if not IBM_SDK_AVAILABLE:
        return {}
    return {
        GenParams.DECODING_METHOD:     "greedy",
        GenParams.MAX_NEW_TOKENS:      600,
        GenParams.MIN_NEW_TOKENS:      50,
        GenParams.TEMPERATURE:         0.1,
        GenParams.REPETITION_PENALTY:  1.1,
        GenParams.STOP_SEQUENCES:      ["\n\nHuman:", "\n\nFaculty:", "---END---"],
    }

# System prompt injected before every query
SYSTEM_PROMPT = """You are EvidenceGuard AI, an expert NBA accreditation assistant for engineering college faculty.

You must answer questions ONLY using the provided context extracted from the NBA Knowledge Base (May 2026 Edition / GAPC v4.0).

Strict Rules:
1. NEVER invent, assume, or fabricate NBA criteria, marks values, or requirements.
2. ALWAYS cite the source section in your answer.
3. If the provided context does not contain the answer, clearly state: "This information is not available in the current knowledge base. Please consult the official NBA SAR manual at https://www.nbaind.org/"
4. When marks differ between Tier-I (Autonomous) and Tier-II (Affiliated), state BOTH values.
5. NEVER certify that a college IS accredited, compliant, or approved.
6. Keep answers structured, accurate, and faculty-friendly.
7. Base EVERY statement on the retrieved context below."""


def _is_configured() -> bool:
    """Returns True only if IBM Cloud credentials are available."""
    return bool(IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID and IBM_SDK_AVAILABLE)


def _build_granite_prompt(question: str, retrieved_chunks: list) -> str:
    """
    Build the full prompt for IBM Granite from the retrieved NBA chunks.
    Uses the <<SYS>> / [INST] style appropriate for Granite instruction models.
    """
    # Build context block from top retrieved chunks
    context_parts = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        context_parts.append(
            f"[Context {i}]\n"
            f"Section: {chunk.get('section', 'Unknown')}\n"
            f"Title: {chunk.get('title', 'Unknown')}\n"
            f"Content: {chunk.get('content', '')}\n"
            f"Source: {chunk.get('source', 'EvidenceGuard AI NBA Knowledge Base')}"
        )
    context_block = "\n\n".join(context_parts) if context_parts else "No relevant context found."

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"=== Retrieved NBA Knowledge Base Context ===\n\n"
        f"{context_block}\n\n"
        f"=== Faculty Question ===\n"
        f"{question}\n\n"
        f"=== EvidenceGuard AI Answer ===\n"
    )
    return prompt


def _get_client():
    """Initialise and return a cached watsonx.ai APIClient."""
    if not _is_configured():
        return None
    try:
        credentials = Credentials(
            url=WATSONX_URL,
            api_key=IBM_CLOUD_API_KEY,
        )
        client = APIClient(credentials)
        return client
    except Exception as exc:
        logger.error("Failed to initialise IBM watsonx.ai client: %s", exc)
        return None


# Module-level cached client (initialized on first call)
_watsonx_client = None
_granite_model   = None


def _get_granite_model():
    """Return a cached IBM Granite ModelInference instance."""
    global _watsonx_client, _granite_model
    if _granite_model is not None:
        return _granite_model

    client = _get_client()
    if client is None:
        return None

    try:
        _granite_model = ModelInference(
            model_id=GRANITE_MODEL_ID,
            params=_build_generation_params(),
            credentials=Credentials(url=WATSONX_URL, api_key=IBM_CLOUD_API_KEY),
            project_id=WATSONX_PROJECT_ID,
        )
        logger.info("IBM Granite model '%s' initialised successfully.", GRANITE_MODEL_ID)
        return _granite_model
    except Exception as exc:
        logger.error("Failed to initialise IBM Granite model: %s", exc)
        return None


def generate_response(question: str, retrieved_chunks: list) -> dict:
    """
    Generate a response using IBM Granite LLM augmentation.

    If IBM credentials are not configured or the SDK is unavailable,
    falls back to returning None so the caller uses TF-IDF synthesis.

    Args:
        question:         The faculty member's NBA question.
        retrieved_chunks: List of retrieved knowledge base chunk dicts.

    Returns:
        dict with keys:
          - answer (str)        : IBM Granite generated answer
          - model (str)         : Model ID used
          - fallback (bool)     : True if local fallback was used
          - sources (list[str]) : Source strings from retrieved chunks
    """
    sources = [c.get("source", "") for c in retrieved_chunks if c.get("source")]

    if not _is_configured():
        logger.info("IBM Granite not configured – using local TF-IDF fallback.")
        return {
            "answer":   None,   # signal to caller: use local synthesis
            "model":    "tfidf_local",
            "fallback": True,
            "sources":  list(dict.fromkeys(sources)),
        }

    model = _get_granite_model()
    if model is None:
        logger.warning("IBM Granite model unavailable – using local TF-IDF fallback.")
        return {
            "answer":   None,
            "model":    "tfidf_local",
            "fallback": True,
            "sources":  list(dict.fromkeys(sources)),
        }

    try:
        prompt = _build_granite_prompt(question, retrieved_chunks)
        response = model.generate_text(prompt=prompt)

        if not response or not response.strip():
            raise ValueError("Empty response from IBM Granite.")

        # Append the official disclaimer
        disclaimer = (
            "\n\n> **Note:** This answer is grounded in the EvidenceGuard AI NBA "
            "Knowledge Base (May 2026 Edition / GAPC v4.0). Always verify against "
            "the official NBA SAR manual at https://www.nbaind.org/ before submitting documents."
        )

        logger.info("IBM Granite response generated successfully (%d chars).", len(response))
        return {
            "answer":   response.strip() + disclaimer,
            "model":    GRANITE_MODEL_ID,
            "fallback": False,
            "sources":  list(dict.fromkeys(sources)),
        }

    except Exception as exc:
        logger.error("IBM Granite generation error: %s – falling back to TF-IDF.", exc)
        return {
            "answer":   None,
            "model":    "tfidf_local",
            "fallback": True,
            "sources":  list(dict.fromkeys(sources)),
        }


def check_granite_connection() -> dict:
    """
    Test IBM Granite / watsonx.ai connectivity.
    Returns a status dict suitable for the /api/health endpoint.
    """
    status = {
        "sdk_installed":    IBM_SDK_AVAILABLE,
        "credentials_set":  bool(IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID),
        "model_id":         GRANITE_MODEL_ID,
        "watsonx_url":      WATSONX_URL,
        "connected":        False,
        "error":            None,
    }

    if not IBM_SDK_AVAILABLE:
        status["error"] = "ibm-watsonx-ai SDK not installed. Run: pip install ibm-watsonx-ai"
        return status

    if not (IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID):
        status["error"] = (
            "IBM Cloud credentials not set. "
            "Please set IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID environment variables."
        )
        return status

    model = _get_granite_model()
    if model is None:
        status["error"] = "Failed to connect to IBM watsonx.ai. Check your API key and project ID."
        return status

    try:
        # Minimal test generation
        test_response = model.generate_text(
            prompt="What is NBA accreditation? Answer in one sentence."
        )
        if test_response and len(test_response.strip()) > 10:
            status["connected"] = True
            logger.info("IBM Granite connectivity test PASSED.")
        else:
            status["error"] = "IBM Granite returned an empty test response."
    except Exception as exc:
        status["error"] = str(exc)
        logger.error("IBM Granite connectivity test FAILED: %s", exc)

    return status
