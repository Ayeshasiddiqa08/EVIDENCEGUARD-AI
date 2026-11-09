"""
EvidenceGuard AI – Guardrails Module
Implements safety, accuracy, and response restriction rules.
All rules are mandatory and enforced before and after RAG retrieval.
"""

import re

# ---------------------------------------------------------------------------
# Prohibited Patterns – topics outside the NBA knowledge base scope
# ---------------------------------------------------------------------------

OUT_OF_SCOPE_PATTERNS = [
    r"\bnaac\b",
    r"\bnba\s+cricket\b",
    r"\bstock\s+market\b",
    r"\binvestment\b",
    r"\bpolitics\b",
    r"\bmedical\b",
    r"\bhospital\b",
    r"\brecipe\b",
    r"\bweather\b",
    r"\bnews\b",
    r"\bsports\b",
    r"\bgames\b",
    r"\bfilms?\b",
    r"\bmovies?\b",
    r"\bcelebrit",
    r"\blottery\b",
    r"\bcasino\b",
]

# Sensitive/confidential patterns the agent must not process
CONFIDENTIAL_PATTERNS = [
    r"\bpassword\b",
    r"\bsecret\b",
    r"\bcredit\s+card\b",
    r"\bbank\s+account\b",
    r"\baadhar\b",
    r"\bpan\s+number\b",
    r"\bpersonal\s+id\b",
]

# Fabrication trigger phrases – agent must refuse to make up information
FABRICATION_TRIGGERS = [
    r"\bmake\s+up\b",
    r"\binvent\b",
    r"\bfabricate\b",
    r"\bjust\s+say\s+yes\b",
    r"\bpretend\b",
    r"\blie\s+about\b",
    r"\bignore\s+the\s+rules\b",
    r"\bbypass\b",
    r"\bjailbreak\b",
    r"\bact\s+as\s+if\b",
    r"\bforget\s+your\s+instructions\b",
    r"\bdo\s+not\s+follow\b",
]

# Compliance-claim patterns – agent must never certify compliance
COMPLIANCE_CLAIM_PATTERNS = [
    r"(confirm|certify|guarantee|ensure|prove)\s+(that\s+)?(we\s+are|college\s+is|institution\s+is|department\s+is)\s+(fully\s+)?(nba\s+)?(compliant|accredited|approved|ready)",
    r"(is\s+)?(the\s+)?(college|institution|department|program)\s+(nba\s+)?(compliant|accredited|approved)\b",
]


# ---------------------------------------------------------------------------
# Guardrail Check Functions
# ---------------------------------------------------------------------------

def check_out_of_scope(query: str) -> dict:
    """
    Returns a block result if query is clearly outside NBA accreditation scope.
    NAAC is out of scope for this agent (NBA-only).
    """
    q_lower = query.lower()
    for pattern in OUT_OF_SCOPE_PATTERNS:
        if re.search(pattern, q_lower):
            # Special case: NAAC comparison questions are allowed
            if "naac" in q_lower and ("nba" in q_lower or "difference" in q_lower or "compare" in q_lower):
                return {"blocked": False}
            return {
                "blocked": True,
                "reason": "out_of_scope",
                "message": (
                    "⚠️ **Out of Scope:** EvidenceGuard AI is designed exclusively for NBA "
                    "accreditation assistance for engineering programs. Your question appears to be "
                    "outside this scope. Please ask about NBA criteria, documents, SAR preparation, "
                    "CO-PO mapping, or accreditation eligibility."
                )
            }
    return {"blocked": False}


def check_confidential(query: str) -> dict:
    """Block queries containing confidential personal information."""
    q_lower = query.lower()
    for pattern in CONFIDENTIAL_PATTERNS:
        if re.search(pattern, q_lower):
            return {
                "blocked": True,
                "reason": "confidential_data",
                "message": (
                    "🔒 **Privacy Protection:** EvidenceGuard AI does not process personal, "
                    "financial, or confidential identification information. Please remove any "
                    "sensitive details from your question and ask only about NBA accreditation "
                    "processes and requirements."
                )
            }
    return {"blocked": False}


def check_fabrication_request(query: str) -> dict:
    """Block attempts to make the agent fabricate or bypass its rules."""
    q_lower = query.lower()
    for pattern in FABRICATION_TRIGGERS:
        if re.search(pattern, q_lower):
            return {
                "blocked": True,
                "reason": "fabrication_attempt",
                "message": (
                    "🚫 **Request Denied:** EvidenceGuard AI cannot fabricate, invent, or "
                    "assume NBA requirements. All answers must be grounded in the official "
                    "NBA Knowledge Base (May 2026 Edition / GAPC v4.0). If information is not "
                    "in the knowledge base, the agent will clearly state that it is unavailable."
                )
            }
    return {"blocked": False}


def check_compliance_claim(query: str) -> dict:
    """
    Detect requests asking agent to certify institutional compliance.
    Agent must never claim a college IS compliant/accredited.
    """
    q_lower = query.lower()
    for pattern in COMPLIANCE_CLAIM_PATTERNS:
        if re.search(pattern, q_lower):
            return {
                "blocked": False,
                "warning": (
                    "⚠️ **Important Disclaimer:** EvidenceGuard AI cannot certify, confirm, or "
                    "guarantee that your institution or program is NBA-compliant or accredited. "
                    "Only the official NBA Peer Team and EAC can determine accreditation status. "
                    "The answer below provides guidance based on the knowledge base only."
                )
            }
    return {"blocked": False}


def check_low_confidence_answer(rag_result: dict) -> dict:
    """
    Post-retrieval guardrail: if confidence is low and retrieved_count is 0,
    add a clear unavailability notice.
    """
    if rag_result.get("confidence") == "low" and rag_result.get("retrieved_count", 0) == 0:
        return {
            "add_notice": True,
            "notice": (
                "ℹ️ **Information Not Found:** The specific information you requested was not found "
                "in the current NBA Knowledge Base. This may mean:\n"
                "- The topic is not covered in the uploaded knowledge base.\n"
                "- The question may need to be rephrased with NBA-specific terminology.\n"
                "- For highly specific queries, please consult the official NBA SAR manual at "
                "https://www.nbaind.org/\n\n"
                "Please try asking about: NBA criteria, SAR documents, CO-PO mapping, SFR, "
                "FDP requirements, or accreditation eligibility."
            )
        }
    return {"add_notice": False}


# ---------------------------------------------------------------------------
# Missing Information Detector
# ---------------------------------------------------------------------------

TIER_KEYWORDS = ["tier", "autonomous", "affiliated", "tier-i", "tier-ii", "tier 1", "tier 2"]
TIER_DIFFERENTIATORS = ["marks", "criteria", "criterion", "score", "evaluation", "weightage"]


def check_tier_missing(query: str) -> dict:
    """
    If the query asks about marks/criteria differences but doesn't specify
    Tier-I or Tier-II, prompt the user to clarify.
    """
    q_lower = query.lower()
    has_tier = any(kw in q_lower for kw in TIER_KEYWORDS)
    needs_tier = any(kw in q_lower for kw in TIER_DIFFERENTIATORS)
    if needs_tier and not has_tier:
        return {
            "needs_clarification": True,
            "clarification_message": (
                "🎓 **Clarification Needed:** Some NBA criteria have different marks for "
                "**Tier-I (Autonomous)** and **Tier-II (Affiliated)** institutions. "
                "To give you the most accurate answer, could you please specify:\n\n"
                "- Is your college **Tier-I (Autonomous / IIT / NIT / IIIT / University Department)**?\n"
                "- Or is it **Tier-II (Affiliated to a State or Central University)**?\n\n"
                "I'll also show you both tiers' information in my answer below."
            )
        }
    return {"needs_clarification": False}


# ---------------------------------------------------------------------------
# Master Guardrail Runner
# ---------------------------------------------------------------------------

def run_input_guardrails(query: str) -> dict:
    """
    Run all input-side guardrails. Returns:
    - {"pass": True} if query is allowed
    - {"pass": False, "message": str} if blocked
    - {"pass": True, "warnings": [...], "clarifications": [...]} if allowed with notices
    """
    warnings = []
    clarifications = []

    # Hard blocks
    for check_fn in [check_out_of_scope, check_confidential, check_fabrication_request]:
        result = check_fn(query)
        if result.get("blocked"):
            return {"pass": False, "message": result["message"]}

    # Soft warnings
    compliance_check = check_compliance_claim(query)
    if compliance_check.get("warning"):
        warnings.append(compliance_check["warning"])

    tier_check = check_tier_missing(query)
    if tier_check.get("needs_clarification"):
        clarifications.append(tier_check["clarification_message"])

    return {"pass": True, "warnings": warnings, "clarifications": clarifications}


def run_output_guardrails(rag_result: dict) -> dict:
    """
    Run output-side guardrails on RAG result.
    Returns the rag_result dict, potentially with a notice prepended.
    """
    low_conf_check = check_low_confidence_answer(rag_result)
    if low_conf_check.get("add_notice"):
        rag_result["answer"] = low_conf_check["notice"]
    return rag_result


def validate_query_length(query: str) -> dict:
    """Ensure query is not empty and within reasonable bounds."""
    stripped = query.strip()
    if not stripped:
        return {"valid": False, "message": "Please enter a question to get started."}
    if len(stripped) < 5:
        return {"valid": False, "message": "Your question is too short. Please provide more detail."}
    if len(stripped) > 2000:
        return {
            "valid": False,
            "message": "Your question is too long (maximum 2000 characters). Please shorten it."
        }
    return {"valid": True}
