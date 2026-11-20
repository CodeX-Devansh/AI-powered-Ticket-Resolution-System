from typing import TypedDict, List, Optional


class TicketState(TypedDict):
    ticket_id: str
    emp_id:str
    title: str
    subject:str
    description:str
    category:str
    priority:str
    answer:str
    sources: List[str]
    retrieved_documents:str
    requires_human_review: bool
    confidence_score:float
    response:str
    human_review_status: str
    human_review_comment: Optional[str]
    final_resolution: Optional[str]
    status:str
    issue: str
    resolution:str
