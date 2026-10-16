from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    """Requête de chat"""
    message: str = Field(..., description="Message de l'utilisateur")
    user_id: str = Field(..., description="ID de l'utilisateur")
    domain: str = Field("general", description="Domaine d'intérêt")
    session_id: Optional[str] = Field(None, description="ID de session")

class ChatResponse(BaseModel):
    """Réponse du chat"""
    reply: str
    session_id: str
    sources: List[Dict[str, Any]] = []
    timestamp: datetime = Field(default_factory=datetime.now)

class UserPreferences(BaseModel):
    """Préférences utilisateur"""
    user_id: str
    domain: str
    email: str
    keywords: List[str] = []
    frequency: str = "daily"