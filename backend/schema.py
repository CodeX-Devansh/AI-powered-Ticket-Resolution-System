from typing import Literal

from pydantic import BaseModel

class TicketCreate(BaseModel):
    title: str
    description: str
    subject: str

class TicketResponse(BaseModel):
    ticket_id:str
    subject:str
    description:str
    status:str
    category:str
    priority:str

class TicketReview(BaseModel):
    action: Literal["approve", "modify"]
    resolution: str | None = None
    comment: str | None = None