# AI-powered-Ticket-Resolution-System
An AI-powered IT Helpdesk system that analyzes support tickets, classifies issues, assigns priority, retrieves relevant knowledge using RAG, generates resolutions, and uses human-in-the-loop review for low-confidence cases.


Tech Stack

* Python
* FastAPI – REST APIs
* LangChain – LLM & RAG
* LangGraph – Agentic workflow & human-in-the-loop
* ChromaDB – Vector store
* MySQL – Application database
* Streamlit – Frontend
* SQLite – LangGraph checkpointing

## Workflow


Ticket
  ↓
Ticket Analysis
  ↓
Classification
  ↓
Priority
  ↓
RAG Retrieval
  ↓
Resolution Generation
  ↓
Confidence Scoring
  ↓
Decision
  ├── High Confidence → Auto Resolve
  │
  └── Low Confidence → Human Review
                            ↓
                         Approval/
                          Modification
                            ↓
                         Resolve


## Project Structure


AgenticAI/
├── backend/
│   ├── main.py
│   ├── model.py
│   ├── schema.py
│   ├── config.py
│   ├── Agents/
│   └── graph/
├── frontend/
│   └── app.py
├── knowledge_base/
├── pyproject.toml
└── README.md


## Run the Project

Install dependencies: 

bash
uv sync


Start the FastAPI backend:

bash
uv run uvicorn backend.main:app --reload


Start the Streamlit frontend in another terminal:

bash
uv run streamlit run frontend/app.py


## URLs

Backend:
http://127.0.0.1:8000


Swagger API Documentation:
http://127.0.0.1:8000/docs

Frontend:
http://localhost:8501


## Human-in-the-Loop

High-confidence tickets are automatically resolved.

Low-confidence tickets pause at LangGraph's `interrupt()` and are sent to the frontend for human review. The reviewer can approve or modify the proposed resolution, after which the workflow resumes and saves the final resolution.
