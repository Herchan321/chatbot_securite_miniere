import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_BASE_URL = "https://api.groq.com/openai/v1"
    GROQ_MODEL = "llama-3.1-8b-instant"
    
    # Paths
    DATA_DIR = "data"
    DB_DIR = "db"
    
    # RAG Parameters
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    RETRIEVER_K = 5
    
    # Model Parameters
    TEMPERATURE = 0.1
    MAX_TOKENS = 1000
    
    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY manquante")
        return True