from backend.graph.state import TicketState


def save_resolve(state: TicketState) -> dict:

    final_resolution = state.get("final_resolution")

    if not final_resolution:
        final_resolution = state.get("resolution")

    if not final_resolution:
        raise ValueError(
            "No final resolution is available."
        )

    return {
        "final_resolution": final_resolution
    }