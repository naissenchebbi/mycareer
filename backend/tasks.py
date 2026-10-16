"""
Tâches Celery pour MyCareer
Automatise l'envoi quotidien des digests
"""
from celery import Celery
from celery.schedules import crontab
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ⚠️ AJOUT : Ajouter le dossier backend au path Python
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Charger .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Créer l'app Celery
celery_app = Celery(
    "mycareer",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Africa/Tunis",
    enable_utc=True,
)

# Planification : tous les jours à 8h du matin
celery_app.conf.beat_schedule = {
    "send-daily-digests": {
        "task": "tasks.send_daily_digests",
        "schedule": crontab(hour=8, minute=0),
    },
}


@celery_app.task
def send_digest_to_user(user_email: str, domain: str = "AI"):
    """Envoie un digest à un utilisateur."""
    print(f"\n📧 Envoi du digest à {user_email}...")
    
    from services.news_service import NewsService
    from services.research_service import ResearchService
    from services.job_service import JobService
    from utils.email_sender import EmailSender
    
    news_service = NewsService()
    research_service = ResearchService()
    job_service = JobService()
    email_sender = EmailSender()
    
    news = news_service.fetch_news("artificial intelligence", max_results=3)
    papers = research_service.fetch_papers(
        "retrieval augmented generation", max_results=3, category="cs.CL"
    )
    jobs = job_service.fetch_jobs("ai", max_results=3)
    
    digest = {"news": news, "papers": papers, "jobs": jobs}
    
    success = email_sender.send_digest(user_email, digest)
    
    if success:
        print(f"✅ Digest envoyé à {user_email}")
        return {"status": "success", "email": user_email}
    else:
        print(f"❌ Échec envoi à {user_email}")
        return {"status": "error", "email": user_email}


@celery_app.task
def send_daily_digests():
    """Envoie les digests à tous les utilisateurs inscrits."""
    print("\n🚀 Lancement des digests quotidiens...")
    
    subscribers = [os.getenv("EMAIL_SENDER", "")]
    
    results = []
    for email in subscribers:
        if email:
            result = send_digest_to_user.delay(email)
            results.append(result.id)
    
    print(f"✅ {len(results)} digests programmés")
    return {"count": len(results), "ids": results}


if __name__ == "__main__":
    print("🧪 Test Celery")