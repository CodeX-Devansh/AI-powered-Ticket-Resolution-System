from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.graph.llm_gateway import embedding, llm
from backend.graph.state import TicketState

BASE_DIR = Path(__file__).resolve().parents[2]

KNOWLEDGE_BASE_DIR = BASE_DIR / "backend" / "knowledge_base"
CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "it_helpdesk_knowledge"

def load_knowledge_base() -> list[Document]:
    """
    Loads all .txt files from the knowledge-base directory.
    """

    if not KNOWLEDGE_BASE_DIR.exists():
        raise FileNotFoundError(
            f"Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}"
        )

    loader = DirectoryLoader(
        path=str(KNOWLEDGE_BASE_DIR),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8"
        },
        show_progress=True,
        use_multithreading=True,
    )

    documents = loader.load()

    if not documents:
        raise ValueError(
            f"No .txt documents found in: {KNOWLEDGE_BASE_DIR}"
        )

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    """
    Splits knowledge-base documents into smaller chunks
    suitable for embedding and retrieval.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    return text_splitter.split_documents(documents)

def get_vector_store() -> Chroma:
    """
    Creates or loads the persistent Chroma vector store.
    """

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding,
        persist_directory=str(CHROMA_DIR),
    )


def build_knowledge_base() -> Chroma:
    """
    Loads the knowledge base, splits the documents,
    generates embeddings, and stores them in Chroma.
    """

    documents = load_knowledge_base()
    chunks = split_documents(documents)

    vector_store = get_vector_store()

    # Prevent duplicate indexing when this function is called again.
    existing_count = vector_store._collection.count()

    if existing_count == 0:
        vector_store.add_documents(chunks)

    return vector_store

def retrieve_documents(
    query: str,
    k: int = 3,
) -> list[Document]:
    """
    Retrieves the most relevant knowledge-base chunks
    for the supplied query.
    """

    if not query or not query.strip():
        raise ValueError("RAG query cannot be empty.")

    vector_store = get_vector_store()

    # Build the vector store if it has not been indexed yet.
    if vector_store._collection.count() == 0:
        vector_store = build_knowledge_base()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": k
        }
    )

    return retriever.invoke(query)

def format_documents(documents: list[Document]) -> str:
    """
    Converts retrieved documents into context for the LLM.
    """

    if not documents:
        return "No relevant knowledge-base information was found."

    formatted_documents = []

    for index, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "Unknown source")

        formatted_documents.append(
            f"Knowledge Source {index}: {source}\n"
            f"{document.page_content}"
        )

    return "\n\n".join(formatted_documents)



RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an IT helpdesk assistant.

Answer the user's question using ONLY the provided
knowledge-base context.

Rules:
- Do not invent troubleshooting steps.
- Do not use information that is not supported by the context.
- If the context does not contain enough information,
  clearly say that the available knowledge base does not
  contain enough information.
- Give clear, practical troubleshooting steps.
- Do not mention internal implementation details.
- Do not mention Chroma, embeddings, LangChain, or RAG.

Knowledge-base context:

{context}
""",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


def generate_answer(
    question: str,
    documents: list[Document],
) -> str:
    """
    Generates an answer using only the retrieved documents.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    context = format_documents(documents)

    chain = (
        RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )


def ask_rag(
    state: TicketState
) -> dict:
    """
    Complete RAG pipeline:

        Question
            ↓
        Retrieve documents
            ↓
        Generate answer
            ↓
        Return answer + sources
    """

    documents = retrieve_documents(
        query=state['issue'],
        k=3,
    )

    answer = generate_answer(
        question=state['issue'],
        documents=documents,
    )
    sources = [
        document.metadata.get("source", "Unknown source")
        for document in documents
    ]

    return {
        "answer": answer,
        "source":sources,
        "retrieved_documents": documents,
    }