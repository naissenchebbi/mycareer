"""
Agrégateur de jobs : combine plusieurs sources
"""
import sys
from pathlib import Path
from typing import List, Dict

sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.job_service import JobService
from services.remotive_service import RemotiveService


class JobAggregator:
    """Combine les offres de plusieurs sources"""
    
    def __init__(self):
        self.remoteok = JobService()
        self.remotive = RemotiveService()
    
    def fetch_all_jobs(self, query: str = "ai", max_per_source: int = 3) -> List[Dict]:
        """
        Récupère les jobs depuis TOUTES les sources.
        
        Args:
            query: Mot-clé (ex: "ai", "python", "data")
            max_per_source: Nombre max par source
        
        Returns:
            Liste combinée (déduplicée par titre)
        """
        print(f"🌐 Agrégation des jobs pour '{query}'...")
        
        all_jobs = []
        
        # Source 1 : RemoteOK
        try:
            remoteok_jobs = self.remoteok.fetch_jobs(query, max_per_source)
            all_jobs.extend(remoteok_jobs)
        except Exception as e:
            print(f"⚠️ RemoteOK échoué: {e}")
        
        # Source 2 : Remotive
        try:
            remotive_jobs = self.remotive.fetch_jobs(query, max_per_source)
            all_jobs.extend(remotive_jobs)
        except Exception as e:
            print(f"⚠️ Remotive échoué: {e}")
        
        # Dédupliquer par titre
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            title_key = job["title"].lower().strip()
            if title_key not in seen:
                seen.add(title_key)
                unique_jobs.append(job)
        
        print(f"  ✅ {len(unique_jobs)} jobs uniques (dédupliqués)")
        return unique_jobs


# === TEST ISOLÉ ===
if __name__ == "__main__":
    print("🧪 Test de l'agrégateur de jobs...\n")
    
    aggregator = JobAggregator()
    jobs = aggregator.fetch_all_jobs("ai", max_per_source=3)
    
    print(f"\n📋 Total : {len(jobs)} jobs\n")
    for i, job in enumerate(jobs, 1):
        source_type = "RemoteOK" if job["id"].startswith("job_") else "Remotive"
        print(f"[{i}] [{source_type}] {job['title']} chez {job['company']}")
    
    print("\n✅ Test terminé !")