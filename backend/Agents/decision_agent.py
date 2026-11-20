from backend.graph.state import TicketState


def decision_agent(state: TicketState) -> dict:
    confidence_score = state["confidence_score"]

    if confidence_score >= 0.80:
        return {
            "requires_human_review": True
        }

    return {
        "requires_human_review": False
    }