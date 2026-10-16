"""
Service Job : récupère les offres d'emploi via RemoteOK API
"""
import requests
from typing import List, Dict
from datetime import datetime


class JobService:
    """Service pour récupérer les offres d'emploi"""
    
    def __init__(self):
        self.base_url = "https://remoteok.com/api"
    
    def fetch_jobs(self, query: str = None, max_results: int = 10) -> List[Dict]:
        """
        Récupère les offres d'emploi depuis RemoteOK (API gratuite).
        """
        print(f"🔍 Recherche jobs (RemoteOK)...")
        
        try:
            headers = {"User-Agent": "MyCareer/1.0"}
            response = requests.get(self.base_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Le premier élément est un metadata, on le skip
            jobs_raw = data[1:] if len(data) > 1 else []
            
            documents = []
            for job in jobs_raw:
                # Filtrer par query si fournie
                if query:
                    title = job.get("position", "").lower()
                    tags = " ".join(job.get("tags", [])).lower()
                    if query.lower() not in title and query.lower() not in tags:
                        continue
                
                description = job.get("description", "")
                # Nettoyer le HTML basique
                description = description.replace("<p>", "").replace("</p>", "")
                description = description.replace("<strong>", "").replace("</strong>", "")
                description = description.replace("<br>", " ").replace("<br/>", " ")
                
                documents.append({
                    "id": f"job_{job.get('id', abs(hash(job.get('url', ''))))}",
                    "content": f"{job.get('position', 'N/A')} chez {job.get('company', 'N/A')}\n\n{description[:500]}",
                    "title": job.get("position", "N/A"),
                    "source": job.get("url", ""),
                    "domain": "Jobs",
                    "company": job.get("company", "N/A"),
                    "location": job.get("location", "Remote"),
                    "tags": job.get("tags", []),
                    "published": job.get("date", datetime.now().isoformat())
                })
                
                if len(documents) >= max_results:
                    break
            
            print(f"  ✅ {len(documents)} offres récupérées")
            return documents
        
        except Exception as e:
            print(f"  ❌ Erreur RemoteOK: {e}")
            return self._mock_jobs(query, max_results)
    
    def _mock_jobs(self, query: str, max_results: int) -> List[Dict]:
        """Données mockées si erreur"""
        return [
            {
                "id": "mock_job_1",
                "content": "AI Engineer chez OpenAI\n\nNous recherchons un AI Engineer...",
                "title": "AI Engineer",
                "source": "https://example.com/job1",
                "domain": "Jobs",
                "company": "OpenAI",
                "location": "Remote",
                "tags": ["python", "ai", "llm"],
                "published": datetime.now().isoformat()
            },
            {
                "id": "mock_job_2",
                "content": "Data Scientist chez Google\n\nNous recherchons un Data Scientist...",
                "title": "Data Scientist",
                "source": "https://example.com/job2",
                "domain": "Jobs",
                "company": "Google",
                "location": "Remote",
                "tags": ["python", "ml"],
                "published": datetime.now().isoformat()
            },
        ][:max_results]


# === TEST ISOLÉ ===
if __name__ == "__main__":
    print("🧪 Test du service Jobs...\n")
    service = JobService()
    
    jobs = service.fetch_jobs("ai", max_results=5)
    
    for i, job in enumerate(jobs, 1):
        print(f"\n[{i}] {job['title']} chez {job.get('company', 'N/A')}")
        print(f"    Location: {job.get('location', 'N/A')}")
        print(f"    Tags: {', '.join(job.get('tags', [])[:3])}")
        print(f"    URL: {job['source']}")
    
    print("\n✅ Test terminé !")