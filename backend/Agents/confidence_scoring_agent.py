from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from backend.graph.llm_gateway import llm
from backend.graph.state import TicketState


def confidence_scoring(state: TicketState) -> dict:
    issue = state["issue"]
    context = state.get("retrieved_documents", "")
    resolution_response = state.get("resolution", "")

    template = """
You are an IT helpdesk resolution evaluator.

Evaluate whether the proposed resolution is fully supported by the
retrieved knowledge-base context.

Compare the proposed resolution against the provided knowledge-base
context.

Evaluation criteria:
- Every troubleshooting step should be supported by the knowledge base.
- Do not give credit for information that is only generally plausible.
- Penalize instructions that are unsupported by the retrieved context.
- Penalize important missing information when the knowledge base clearly
  provides it.
- Do not evaluate whether the resolution is well-written.
- Evaluate only whether the resolution is grounded in the provided
  knowledge-base context.

Return ONLY ONE decimal number between 0.0 and 1.0.

Do not return explanations.
Do not return markdown.
Do not return words.
Do not return labels.
Do not return a percentage.

Where:
1.0 = Fully supported by the retrieved knowledge base
0.8–0.99 = Almost fully supported, with minor unsupported or unclear details
0.6–0.79 = Partially supported
0.3–0.59 = Weakly supported
0.0–0.29 = Mostly or completely unsupported

Ticket issue:
{issue}

Retrieved knowledge-base context:
{context}

Proposed resolution:
{resolution}

Grounding score:
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["issue", "context", "resolution"]
    )

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke(
        {
            "issue": issue,
            "context": context,
            "resolution": resolution_response
        }
    )

    try:
        confidence_score = float(response.strip())
    except ValueError:
        raise ValueError(
            f"Confidence scoring agent returned an invalid score: {response!r}"
        )

    if not 0.0 <= confidence_score <= 1.0:
        raise ValueError(
            f"Confidence score must be between 0.0 and 1.0, "
            f"but received: {confidence_score}"
        )

    return {
        "confidence_score": confidence_score
    }