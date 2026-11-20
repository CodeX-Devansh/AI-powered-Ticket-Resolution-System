from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from backend.graph.llm_gateway import llm
from backend.graph.state import TicketState


def resolution_agent(state: TicketState)-> dict:
    description=state['description']
    subject=state['subject']
    title=state['title']
    context=state.get('retrieved_documents')
    template="""
    You are an IT helpdesk ticket analysis assistant.

Analyze the user's ticket using the subject, title, and description and RAG context.

Your task is to generate the proposed resolution/troubleshooting.

Subject: {subject}

Title: {title}

Description: {description}

RAG context: {context}

Instructions:
- Understand the incident using the subject, title, description, and retrieved
  knowledge-base context.
- Use the retrieved knowledge-base information as the primary source for the
  proposed resolution.
- Provide practical troubleshooting and resolution steps relevant to the incident.
- If the knowledge-base context contains an applicable resolution, adapt it to
  the user's specific incident.
- Do not invent technical details, system information, error messages, or
  troubleshooting steps that are unsupported by the ticket or retrieved context.
- Do not classify the incident.
- Do not assign or modify the incident priority.
- Do not calculate a score.
- Do not mention the RAG process or retrieved documents in the final response.
- If the retrieved context does not contain enough information to determine a
  reliable resolution, clearly state that additional investigation or information
  is required rather than inventing a solution.
- Keep the resolution concise, clear, and actionable.
- Return only the proposed resolution/troubleshooting steps.

Proposed Resolution:
    """
    prompt= PromptTemplate(
        template=template, input_variables=["title", "subject", "description", "context"]
    )
    chain= prompt|llm|StrOutputParser()
    response= chain.invoke(
        {"title": title, "subject": subject, "description": description, "context":context}
    )
    return {"resolution":response}