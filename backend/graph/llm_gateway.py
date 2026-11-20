import os

from langchain_cohere import CohereEmbeddings, ChatCohere
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")
llm= ChatCohere(cohere_api_key=api_key, model="command-a-03-2025", temperature=0.7)
embedding= CohereEmbeddings(cohere_api_key=api_key,model="embed-english-v3.0")