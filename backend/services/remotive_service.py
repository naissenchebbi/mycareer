"""
Service Remotive : offres d'emploi remote
"""
import requests
from typing import List, Dict
from datetime import datetime


class RemotiveService:
    """Service pour récupérer les offres d'emploi via Remotive API"""
    
    def __init__(self):
        self.base_url = "https://remotive.com/api/remote-jobs"
    
    def fetch_jobs(self, query: str = None, max_results: int = 10) -> List[Dict]:
        """Récupère les offres d'emploi depuis Remotive"""
        print(f"🔍 Recherche jobs (Remotive)...")
        
        params = {}
        if query:
            params["search"] = query
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            documents = []
            for job in data.get("jobs", [])[:max_results]:
                documents.append({
                    "id": f"remotive_{job.get('id')}",
                    "content": f"{job.get('title', 'N/A')} chez {job.get('company_name', 'N/A')}\n\n{job.get('description', '')[:500]}",
                    "title": job.get("title", "N/A"),
                    "source": job.get("url", ""),
                    "domain": "Jobs",
                    "company": job.get("company_name", "N/A"),
                    "location": job.get("candidate_required_location", "Remote"),
                    "tags": job.get("tags", []),
                    "published": job.get("publication_date", datetime.now().isoformat())
                })
            
            print(f"  ✅ {len(documents)} offres récupérées")
            return documents
        
        except Exception as e:
            print(f"  ❌ Erreur Remotive: {e}")
            return []


# === TEST ISOLÉ ===
if __name__ == "__main__":
    print("🧪 Test du service Remotive...\n")
    service = RemotiveService()
    jobs = service.fetch_jobs("python", max_results=5)
    
    for i, job in enumerate(jobs, 1):
        print(f"\n[{i}] {job['title']} chez {job['company']}")
        print(f"    Location: {job['location']}")
        print(f"    URL: {job['source']}")
    
    print("\n✅ Test terminé !")