from agent.types import Intent


ESCALATION_KEYWORDS = [
    "human",
    "agent",
    "representative",
    "complaint",
    "legal",
    "urgent",
    "angry",
    "manager",
    "escalate",
    "lawsuit",
]

SUMMARY_KEYWORDS = [
    "summarize",
    "summary",
    "what have we tried",
    "recap",
]

TROUBLESHOOTING_KEYWORDS = [
    "not working",
    "can't",
    "cannot",
    "failed",
    "error",
    "issue",
    "problem",
    "broken",
    "reset",
    "login",
    "password",
    "email not received",
]

POLICY_KEYWORDS = [
    "refund",
    "cancel",
    "billing",
    "invoice",
    "trial",
    "policy",
    "plan",
    "delete account",
    "data deletion",
]


def classify_intent(query: str) -> Intent:
    q = query.lower()

    if any(k in q for k in ESCALATION_KEYWORDS):
        return Intent.ESCALATION
    if any(k in q for k in SUMMARY_KEYWORDS):
        return Intent.SUMMARIZATION
    if any(k in q for k in TROUBLESHOOTING_KEYWORDS):
        return Intent.TROUBLESHOOTING
    if any(k in q for k in POLICY_KEYWORDS):
        return Intent.POLICY_PROCESS
    if "how" in q or "what" in q or "can i" in q:
        return Intent.KNOWLEDGE_BASE

    return Intent.UNKNOWN
