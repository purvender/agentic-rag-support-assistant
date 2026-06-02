from agent.memory import add_turn, update_issue_summary
from agent.router import classify_intent
from agent.tools import (
    draft_final_response,
    escalate_to_human,
    retrieve_kb,
    search_similar_issues,
    summarize_conversation,
)
from agent.types import ConversationState, Intent, RetrievedDoc


def run_agent(query: str, history=None) -> ConversationState:
    state = ConversationState(user_query=query, history=history or [])
    add_turn(state, "user", query)

    state.intent = classify_intent(query)

    if state.intent == Intent.SUMMARIZATION:
        summary_result = summarize_conversation(state)
        state.issue_summary = summary_result.content

    elif state.intent == Intent.ESCALATION:
        update_issue_summary(state, query)
        summary = summarize_conversation(state)
        escalation = escalate_to_human(
            "User requested human support or request is high-risk.",
            summary.content,
        )
        state.escalation_reason = escalation.metadata.get("reason")

    else:
        retrieval = retrieve_kb(query)
        similar = search_similar_issues(query)

        if retrieval.success:
            docs = retrieval.metadata.get("docs", [])
            state.retrieved_docs = [
                RetrievedDoc(
                    source=d.get("source", "unknown"),
                    content=d.get("content", ""),
                    score=d.get("score"),
                )
                for d in docs
            ]

        if not state.retrieved_docs and state.intent in [Intent.TROUBLESHOOTING, Intent.UNKNOWN]:
            state.needs_clarification = True

        update_issue_summary(state, query)

        if similar.success and similar.content and "No similar issue database connected yet." not in similar.content:
            update_issue_summary(state, similar.content)

    final = draft_final_response(state)
    state.final_response = final.content
    add_turn(state, "assistant", state.final_response)
    return state
