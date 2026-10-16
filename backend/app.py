from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
import logging

from config import config
from models.schemas import ChatRequest, ChatResponse
from rag.pipeline import RAGPipeline
from services.ingestion import IngestionService
from services.news_service import NewsService
from services.research_service import ResearchService
from services.job_aggregator import JobAggregator

# === LOGGING ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === APPLICATION ===
app = FastAPI(
    title="MyCareer AI Assistant",
    version="1.0.0"
)

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === INITIALISATION DU RAG ===
logger.info("🚀 Initialisation du pipeline RAG...")
rag_pipeline = RAGPipeline()

# === INGESTION AUTOMATIQUE (seulement si base vide) ===
logger.info("📥 Initialisation du service d'ingestion...")
ingestion = IngestionService(rag_pipeline)

try:
    count = rag_pipeline.retriever.collection.count()
    
    if count == 0:
        logger.info("📥 Base vide → ingestion des papiers ArXiv...")
        ingestion.ingest_arxiv(
            "retrieval augmented generation",
            category="cs.CL",
            max_results=5
        )
        logger.info("✅ RAG initialisé avec les papiers ArXiv")
    else:
        logger.info(f"✅ Base déjà remplie ({count} documents) → pas d'ingestion")
except Exception as e:
    logger.error(f"❌ Erreur ingestion: {e}")

# === SERVICES ===
news_service = NewsService()
research_service = ResearchService()
job_service = JobAggregator()
# === SESSIONS ===
sessions = {}


# === ROUTES ===

@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur MyCareer AI Assistant",
        "status": "online",
        "version": "1.0.0",
        "rag_status": "ready"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "rag": "operational"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint de chat avec RAG"""
    try:
        logger.info(f"Message de {request.user_id}: {request.message[:50]}")
        
        # Gestion session
        session_id = request.session_id or str(uuid.uuid4())
        if session_id not in sessions:
            sessions[session_id] = {"history": []}
        
        sessions[session_id]["history"].append({
            "role": "user",
            "content": request.message
        })
        
        # === UTILISER LE RAG ===
        result = rag_pipeline.query(
            question=request.message,
            top_k=5,
            domain=request.domain
        )
        
        reply = result["answer"]
        
        sessions[session_id]["history"].append({
            "role": "assistant",
            "content": reply
        })
        
        return ChatResponse(
            reply=reply,
            session_id=session_id,
            sources=result["sources"]
        )
        
    except Exception as e:
        logger.error(f"Erreur: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/digest/{user_id}")
async def get_digest(user_id: str, domain: str = "AI"):
    """
    Génère un digest quotidien : news + papiers + jobs
    """
    try:
        logger.info(f"Génération du digest pour {user_id} (domaine: {domain})")
        
        # 1. News
        news = news_service.fetch_news("artificial intelligence", max_results=3)
        
        # 2. Papiers
        papers = research_service.fetch_papers(
            "retrieval augmented generation",
            max_results=10,
            category="cs.CL"
        )
        
        # 3. Jobs
        jobs = job_service.fetch_all_jobs("ai", max_per_source=3)

        
        # 4. Digest
        digest = {
            "user_id": user_id,
            "date": datetime.now().isoformat(),
            "domain": domain,
            "news": [
                {
                    "title": n["title"],
                    "source": n.get("source", ""),
                    "published": n.get("published", "")
                } for n in news
            ],
            "papers": [
                {
                    "title": p["title"],
                    "authors": p.get("authors", []),
                    "source": p.get("source", ""),
                    "published": p.get("published", "")
                } for p in papers
            ],
            "jobs": [
                {
                    "title": j["title"],
                    "company": j.get("company", ""),
                    "location": j.get("location", "Remote"),
                    "source": j.get("source", "")
                } for j in jobs
            ],
            "summary": f"Digest du {datetime.now().strftime('%d/%m/%Y')} - {len(news)} news + {len(papers)} papiers + {len(jobs)} jobs"
        }
        
        return digest
    
    except Exception as e:
        logger.error(f"Erreur digest: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Récupérer l'historique d'une session"""
    if session_id not in sessions:
        raise HTTPException(404, "Session non trouvée")
    return {
        "session_id": session_id,
        "history": sessions[session_id]["history"],
        "length": len(sessions[session_id]["history"])
    }

from pydantic import BaseModel

class SubscribeRequest(BaseModel):
    email: str
    domain: str = "AI"


@app.post("/api/subscribe")
async def subscribe(request: SubscribeRequest):
    """Inscrit un utilisateur au digest quotidien."""
    try:
        logger.info(f"Inscription de {request.email}")
        
        from tasks import send_digest_to_user
        
        result = send_digest_to_user.delay(request.email, request.domain)
        
        return {
            "status": "success",
            "message": f"Inscription confirmée. Digest envoyé à {request.email}",
            "task_id": result.id
        }
    except Exception as e:
        logger.error(f"Erreur subscribe: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# === LANCEMENT ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG
    )