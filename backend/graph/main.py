import sqlite3

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from backend.Agents.confidence_scoring_agent import confidence_scoring
from backend.Agents.decision_agent import decision_agent
from backend.Agents.resolution_agent import resolution_agent
from backend.Agents.save_resolve import save_resolve
from backend.Agents.ticket_analyzer import ticket_analyzer
from backend.Agents.classification_agent import classification_agent
from backend.Agents.priority_agent import priority_agent
from backend.Agents.RAG import ask_rag
from backend.Agents.human_review import human_review

from backend.graph.state import TicketState


def route_after_decision(state: TicketState) -> str:

    if state.get("requires_human_review"):
        return "human_review"

    return "save_resolve"


builder = StateGraph(TicketState)


builder.add_node(
    "ticket_analyzer",
    ticket_analyzer
)

builder.add_node(
    "classification_agent",
    classification_agent
)

builder.add_node(
    "priority_agent",
    priority_agent
)

builder.add_node(
    "rag",
    ask_rag
)

builder.add_node(
    "resolution",
    resolution_agent
)

builder.add_node(
    "confidence_calculation",
    confidence_scoring
)

builder.add_node(
    "decision",
    decision_agent
)

builder.add_node(
    "human_review",
    human_review
)

builder.add_node(
    "save_resolve",
    save_resolve
)

builder.add_edge(
    START,
    "ticket_analyzer"
)

builder.add_edge(
    "ticket_analyzer",
    "classification_agent"
)

builder.add_edge(
    "classification_agent",
    "priority_agent"
)

builder.add_edge(
    "priority_agent",
    "rag"
)

builder.add_edge(
    "rag",
    "resolution"
)

builder.add_edge(
    "resolution",
    "confidence_calculation"
)

builder.add_edge(
    "confidence_calculation",
    "decision"
)


builder.add_conditional_edges(
    "decision",
    route_after_decision,
    {
        "human_review": "human_review",
        "save_resolve": "save_resolve"
    }
)


builder.add_edge(
    "human_review",
    "save_resolve"
)


builder.add_edge(
    "save_resolve",
    END
)

connection = sqlite3.connect(
    "langgraph_checkpoints.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(connection)


graph = builder.compile(
    checkpointer=checkpointer
)