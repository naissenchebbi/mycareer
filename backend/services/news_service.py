"""
Service NewsAPI pour récupérer les actualités
"""
import os
import requests
from typing import List, Dict
from datetime import datetime, timedelta


class NewsService:
    """Service pour récupérer les actualités via NewsAPI"""
    
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY", "")
        self.base_url = "https://newsapi.org/v2/everything"
    
    def fetch_news(self, query: str, max_results: int = 10, language: str = "en") -> List[Dict]:
        """Récupère les actualités les plus récentes."""
        if not self.api_key:
            print("⚠️ NEWS_API_KEY manquante → données mockées")
            return self._mock_news(query, max_results)
        
        print(f"🔍 Recherche NewsAPI: '{query}' (max {max_results})")
        
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        params = {
            "q": query,
            "from": from_date,
            "sortBy": "publishedAt",
            "language": language,
            "pageSize": max_results,
            "apiKey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            documents = []
            for article in data.get("articles", []):
                if not article.get("description"):
                    continue
                
                documents.append({
                    "id": f"news_{abs(hash(article['url'])) % 1000000}",
                    "content": f"{article['title']}\n\n{article['description']}",
                    "title": article["title"],
                    "source": article["url"],
                    "domain": "AI",
                    "published": article["publishedAt"],
                    "author": article.get("author", "Unknown")
                })
            
            print(f"  ✅ {len(documents)} articles récupérés")
            return documents
        
        except Exception as e:
            print(f"  ❌ Erreur NewsAPI: {e}")
            return self._mock_news(query, max_results)
    
    def _mock_news(self, query: str, max_results: int) -> List[Dict]:
        """Données mockées si pas de clé API"""
        return [
            {
                "id": "mock_news_1",
                "content": "OpenAI annonce GPT-5 avec des capacités de raisonnement améliorées.",
                "title": "OpenAI lance GPT-5",
                "source": "https://example.com/gpt5",
                "domain": "AI",
                "published": datetime.now().isoformat(),
                "author": "John Doe"
            },
        ][:max_results]


# === TEST ISOLÉ ===
if __name__ == "__main__":
    from dotenv import load_dotenv
    from pathlib import Path
    
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    print(f"🔑 Clé API chargée: {os.getenv('NEWS_API_KEY', 'VIDE')[:10]}...\n")
    
    print("🧪 Test du service NewsAPI...\n")
    service = NewsService()
    
    news = service.fetch_news("artificial intelligence", max_results=3)
    
    for i, article in enumerate(news, 1):
        print(f"\n[{i}] {article['title']}")
        print(f"    Source: {article['source']}")
        print(f"    Publié: {article['published'][:10]}")
    
    print("\n✅ Test terminé !")