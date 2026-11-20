from sqlalchemy import Column, Integer, String, Float, Text
from backend.config import Base, engine

class Ticket(Base):
    __tablename__="tickets"
    id = Column(Integer, primary_key=True)
    ticket_id= Column(String(50), unique=True, nullable=False)
    title = Column(String(225), nullable=False)
    subject = Column(String(225), nullable=False)
    description= Column(Text, nullable=False)
    status = Column(String(225),nullable=False)
    confidence_score= Column(Float, nullable=True)
    category = Column(String(225), nullable=True)
    priority = Column(String(225), nullable=True)
    resolution = Column(Text, nullable=True)

Base.metadata.create_all(engine)