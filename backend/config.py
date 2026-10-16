import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de l'application MyCareer"""
    
    # === API Keys ===
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
    
    # === Base de données vectorielle ===
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    COLLECTION_NAME = "mycareer_knowledge"
    
    # === Modèles IA ===
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    LLM_MODEL = "gpt-3.5-turbo"
    
    # === Application ===
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    
    # === CORS ===
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

config = Config()