from langgraph.types import interrupt

from backend.graph.state import TicketState


def human_review(state: TicketState) -> dict:

    review = interrupt({
        "ticket_id": state["ticket_id"],
        "resolution": state["resolution"],
        "confidence_score": state["confidence_score"],
        "message": "Please review the proposed resolution."
    })

    action = review.get("action")

    if action == "approve":
        return {
            "resolution": state["resolution"],
            "status": "resolved"
        }

    if action == "modify":
        return {
            "resolution": review["resolution"],
            "status": "resolved"
        }

    if action == "reject":
        return {
            "status": "pending"
        }

    raise ValueError(f"Invalid review action: {action}")