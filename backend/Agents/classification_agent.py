from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from backend.graph.llm_gateway import llm
from backend.graph.state import TicketState


def classification_agent(state: TicketState)-> dict:
    description=state['description']
    subject=state['subject']
    title=state['title']
    template="""
    You are a helpful assistant which analyzes the ticket using subject, title, and description to classify the ticket.
    Only provide the category the ticket belongs to.
    subject: {subject}
    title: {title}
    description: {description}
    """
    prompt= PromptTemplate.from_template(
        template=template
    )
    chain= prompt|llm| StrOutputParser()
    response= chain.invoke(
        {"title": title, "subject": subject, "description": description}
    )
    return {"category":response}