from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from backend.graph.llm_gateway import llm
from backend.graph.state import TicketState


def priority_agent(state: TicketState)-> dict:
    description=state['description']
    subject=state['subject']
    title=state['title']
    template="""
    You are an IT helpdesk assistant who analyzes the ticket using subject, title, and description to classify the ticket priority.
    Determine whether the issue is Low, Medium, High, or Critical.
    subject: {subject}
    title: {title}
    description: {description}
    Only assign/ return the priority of the ticket.
    """
    prompt= PromptTemplate(
        template=template, input_variables=["title", "subject", "description"]
    )
    chain= prompt|llm|StrOutputParser()
    response= chain.invoke(
        {"title": title, "subject": subject, "description": description}
    )
    return {"priority":response}