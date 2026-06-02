from agent.types import ConversationState, ConversationTurn


def add_turn(state: ConversationState, role: str, message: str) -> None:
    state.history.append(ConversationTurn(role=role, message=message))


def update_issue_summary(state: ConversationState, new_info: str) -> None:
    if not state.issue_summary:
        state.issue_summary = new_info.strip()
    elif new_info.strip() not in state.issue_summary:
        state.issue_summary = f"{state.issue_summary} | {new_info.strip()}"


def add_attempted_step(state: ConversationState, step: str) -> None:
    normalized = step.strip().lower()
    existing = {s.strip().lower() for s in state.attempted_steps}
    if normalized and normalized not in existing:
        state.attempted_steps.append(step.strip())
