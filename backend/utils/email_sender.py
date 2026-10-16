"""
Service d'envoi d'emails via Gmail SMTP
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
from datetime import datetime


class EmailSender:
    """Service pour envoyer des emails via Gmail"""

    def __init__(self):
        self.sender = os.getenv("EMAIL_SENDER", "")
        self.password = os.getenv("EMAIL_PASSWORD", "")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_digest(self, recipient: str, digest: Dict) -> bool:
        """Envoie un digest par email."""
        if not self.sender or not self.password:
            print("[WARN] EMAIL_SENDER ou EMAIL_PASSWORD manquants")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"MyCareer - Digest du {datetime.now().strftime('%d/%m/%Y')}"
            msg["From"] = self.sender
            msg["To"] = recipient

            html = self._build_html(digest)
            msg.attach(MIMEText(html, "html", "utf-8"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)

            print(f"[OK] Email envoye a {recipient}")
            return True

        except Exception as e:
            print(f"[ERROR] Erreur : {e}")
            return False

    def _build_html(self, digest: Dict) -> str:
        """Construit le HTML du digest."""

        # === NEWS ===
        news_html = ""
        for n in digest.get("news", []):
            title = n.get("title", "Sans titre")
            source = n.get("source", "#")
            news_html += f"""
            <div style="margin-bottom:15px;padding:12px;background:#f5f7fa;border-left:4px solid #3b82f6;border-radius:8px;">
                <h4 style="margin:0 0 5px 0;color:#222;">&#128240; {title}</h4>
                <a href="{source}" style="color:#3b82f6;font-size:13px;text-decoration:none;">Lire la suite &rarr;</a>
            </div>
            """

        # === PAPERS ===
        papers_html = ""
        for p in digest.get("papers", []):
            title = p.get("title", "Sans titre")
            source = p.get("source", "#")
            authors = ", ".join(p.get("authors", [])[:3]) if p.get("authors") else "N/A"
            papers_html += f"""
            <div style="margin-bottom:15px;padding:12px;background:#f5f7fa;border-left:4px solid #8b5cf6;border-radius:8px;">
                <h4 style="margin:0 0 5px 0;color:#222;">&#128196; {title}</h4>
                <p style="margin:0 0 5px 0;color:#666;font-size:13px;">&#128101; {authors}</p>
                <a href="{source}" style="color:#8b5cf6;font-size:13px;text-decoration:none;">Voir le papier &rarr;</a>
            </div>
            """

        # === JOBS ===
        jobs_html = ""
        for j in digest.get("jobs", []):
            title = j.get("title", "Sans titre")
            source = j.get("source", "#")
            company = j.get("company", "N/A")
            location = j.get("location", "Remote")
            jobs_html += f"""
            <div style="margin-bottom:15px;padding:12px;background:#f5f7fa;border-left:4px solid #10b981;border-radius:8px;">
                <h4 style="margin:0 0 5px 0;color:#222;">&#128188; {title}</h4>
                <p style="margin:0 0 5px 0;color:#666;font-size:13px;">&#127970; {company} &bull; &#128205; {location}</p>
                <a href="{source}" style="color:#10b981;font-size:13px;text-decoration:none;">Voir l'offre &rarr;</a>
            </div>
            """

        # === HTML COMPLET ===
        html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:600px;margin:0 auto;padding:20px;background:#fff;">

    <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:30px;border-radius:12px;text-align:center;margin-bottom:30px;">
        <h1 style="color:white;margin:0;font-size:26px;">&#129517; MyCareer</h1>
        <p style="color:rgba(255,255,255,0.9);margin:10px 0 0 0;font-size:14px;">
            Votre digest du {datetime.now().strftime('%d/%m/%Y')}
        </p>
    </div>

    <h2 style="color:#333;margin-top:30px;font-size:18px;border-bottom:2px solid #3b82f6;padding-bottom:8px;">
        &#128240; Actualites ({len(digest.get('news', []))})
    </h2>
    {news_html if news_html else '<p style="color:#999;font-style:italic;">Aucune actualite</p>'}

    <h2 style="color:#333;margin-top:30px;font-size:18px;border-bottom:2px solid #8b5cf6;padding-bottom:8px;">
        &#128196; Papiers de recherche ({len(digest.get('papers', []))})
    </h2>
    {papers_html if papers_html else '<p style="color:#999;font-style:italic;">Aucun papier</p>'}

    <h2 style="color:#333;margin-top:30px;font-size:18px;border-bottom:2px solid #10b981;padding-bottom:8px;">
        &#128188; Offres d'emploi ({len(digest.get('jobs', []))})
    </h2>
    {jobs_html if jobs_html else '<p style="color:#999;font-style:italic;">Aucune offre</p>'}

    <div style="margin-top:40px;padding-top:20px;border-top:1px solid #eee;text-align:center;color:#999;font-size:12px;">
        <p>&copy; 2026 MyCareer - AI Career Assistant</p>
    </div>
</body>
</html>
        """

        return html


# === TEST ISOLE ===
if __name__ == "__main__":
    from dotenv import load_dotenv
    from pathlib import Path

    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    print("Test de l'envoi d'email...\n")

    sender = EmailSender()

    test_digest = {
        "news": [
            {"title": "Test news 1", "source": "https://example.com/news1"},
            {"title": "Test news 2", "source": "https://example.com/news2"},
        ],
        "papers": [
            {"title": "Test paper", "authors": ["Author 1", "Author 2"], "source": "https://arxiv.org/abs/1234"},
        ],
        "jobs": [
            {"title": "AI Engineer", "company": "Test Corp", "location": "Remote", "source": "https://example.com/job"},
        ],
    }

    recipient = "nchebbi755@gmail.com"

    success = sender.send_digest(recipient, test_digest)

    if success:
        print("\nVerifie ta boite mail !")
    else:
        print("\nEchec.")