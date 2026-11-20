from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from backend.graph.llm_gateway import llm
from backend.graph.state import TicketState


def ticket_analyzer(state: TicketState)-> dict:
    description=state['description']
    subject=state['subject']
    title=state['title']
    template="""
You are an IT helpdesk ticket analysis assistant.

Analyze the user's ticket using the subject, title, and description.

Your task is to identify and clearly describe the actual technical issue reported by the user.

Instructions:
- Understand the user's problem from the provided information.
- Remove unnecessary conversational words and irrelevant details.
- Preserve important technical details, symptoms, errors, and affected systems.
- Do not suggest a solution or troubleshooting steps.
- Do not classify the ticket.
- Do not assign priority.
- Do not assume information that is not present in the ticket.
- If the information is ambiguous, describe the issue only using what is explicitly provided.
- Return only a concise issue statement suitable for use as a knowledge-base retrieval query.

Subject: {subject}

Title: {title}

Description: {description}
    """
    prompt= PromptTemplate(
        template=template, input_variables=["title", "subject", "description"]
    )
    chain= prompt|llm|StrOutputParser()
    response= chain.invoke(
        {"title": title, "subject": subject, "description": description}
    )
    return {"issue":response}