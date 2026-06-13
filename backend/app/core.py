from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from .config import settings

# LLM model
llm = ChatGroq(
    model=settings.llm_model,
    temperature=0.2,
    api_key=settings.groq_api_key,
)

# Embedding for RAG ingestion and retrieval.
embedding = OllamaEmbeddings(model=settings.embed_model)