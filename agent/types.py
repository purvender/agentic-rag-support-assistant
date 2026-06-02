from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class Intent(str, Enum):
    KNOWLEDGE_BASE = "knowledge_base"
    TROUBLESHOOTING = "troubleshooting"
    POLICY_PROCESS = "policy_process"
    ESCALATION = "escalation"
    SUMMARIZATION = "summarization"
    UNKNOWN = "unknown"


@dataclass
class RetrievedDoc:
    source: str
    content: str
    score: Optional[float] = None


@dataclass
class ToolResult:
    tool_name: str
    success: bool
    content: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class ConversationTurn:
    role: str
    message: str


@dataclass
class ConversationState:
    user_query: str
    history: List[ConversationTurn] = field(default_factory=list)
    intent: Intent = Intent.UNKNOWN
    issue_summary: str = ""
    attempted_steps: List[str] = field(default_factory=list)
    retrieved_docs: List[RetrievedDoc] = field(default_factory=list)
    needs_clarification: bool = False
    escalation_reason: Optional[str] = None
    final_response: str = ""
