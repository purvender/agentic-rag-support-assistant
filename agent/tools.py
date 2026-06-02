from agent.types import ConversationState, ToolResult


def retrieve_kb(query: str) -> ToolResult:
    try:
        from scripts.rag_query import retrieve_context_only

        docs = retrieve_context_only(query)
        retrieved = [
            {
                "source": d.get("source", "unknown"),
                "content": d.get("content", ""),
                "score": d.get("score"),
            }
            for d in docs
        ]
        return ToolResult(
            tool_name="retrieve_kb",
            success=True,
            content="Retrieved knowledge base context.",
            metadata={"docs": retrieved},
        )
    except Exception as e:
        return ToolResult(
            tool_name="retrieve_kb",
            success=False,
            content=f"Retrieval failed: {e}",
        )


def summarize_conversation(state: ConversationState) -> ToolResult:
    summary_parts = []
    if state.issue_summary:
        summary_parts.append(f"Issue: {state.issue_summary}")
    if state.attempted_steps:
        summary_parts.append("Tried: " + ", ".join(state.attempted_steps))
    if not summary_parts and state.history:
        summary_parts.append(
            "Conversation turns: "
            + " | ".join(f"{t.role}: {t.message}" for t in state.history[-6:])
        )
    summary = "\n".join(summary_parts) if summary_parts else "No conversation summary available."
    return ToolResult(
        tool_name="summarize_conversation",
        success=True,
        content=summary,
    )


def search_similar_issues(query: str) -> ToolResult:
    mock_hits = []
    q = query.lower()
    if "refund" in q:
        mock_hits.append("Past cases often depend on the annual refund window.")
    if "password" in q or "reset" in q:
        mock_hits.append("Past cases often involve checking spam and verifying the login email.")
    content = "\n".join(mock_hits) if mock_hits else "No similar issue database connected yet."
    return ToolResult(
        tool_name="search_similar_issues",
        success=True,
        content=content,
    )


def escalate_to_human(reason: str, conversation_summary: str) -> ToolResult:
    return ToolResult(
        tool_name="escalate_to_human",
        success=True,
        content="Escalation prepared for human support.",
        metadata={
            "reason": reason,
            "summary": conversation_summary,
            "ticket_created": False,
        },
    )


def draft_final_response(state: ConversationState) -> ToolResult:
    retrieved_context = (
        "\n\n".join([f"[{d.source}] {d.content}" for d in state.retrieved_docs])
        or "No retrieved context."
    )

    response = []

    if state.needs_clarification:
        response.append("I need one more detail before I can answer accurately.")
        response.append(
            "Please share the exact error, the affected email/account, and what you have already tried."
        )
    elif state.intent.value == "summarization":
        response.append("Here is a summary of the conversation so far:")
        response.append(state.issue_summary or "No summary available yet.")
        if state.attempted_steps:
            response.append("Steps already tried: " + ", ".join(state.attempted_steps))
    elif state.escalation_reason:
        response.append("This should be handed to a human support agent.")
        response.append(f"Reason: {state.escalation_reason}")
        if state.issue_summary:
            response.append(f"Summary: {state.issue_summary}")
    else:
        if state.retrieved_docs:
            response.append("Based on the available support information:")
            response.append(retrieved_context[:1500])
        else:
            response.append("I could not find grounded support context for this request.")
            response.append("Please provide a little more detail so I can guide you safely.")

        if state.attempted_steps:
            response.append(
                "I will avoid repeating steps you already tried: "
                + ", ".join(state.attempted_steps)
            )

    return ToolResult(
        tool_name="draft_final_response",
        success=True,
        content="\n\n".join(response),
    )
