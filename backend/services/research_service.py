"""
Service ArXiv pour récupérer les papiers de recherche
"""
import arxiv
from typing import List, Dict
from datetime import datetime


class ResearchService:
    """Service pour récupérer les papiers de recherche depuis ArXiv"""
    
    def __init__(self, max_results: int = 10):
        self.max_results = max_results
        self.client = arxiv.Client()
    
    def fetch_papers(self, query: str, max_results: int = None, category: str = None) -> List[Dict]:
        """
        Récupère les papiers les plus récents depuis ArXiv.
        
        Args:
            query: Mot-clé de recherche
            max_results: Nombre max de papiers
            category: Catégorie ArXiv (ex: "cs.CL", "cs.AI")
        """
        max_results = max_results or self.max_results
        
        # Construire la requête
        if category:
            full_query = f'cat:{category} AND abs:"{query}"'
        else:
            full_query = f'abs:"{query}"'
        
        print(f"🔍 Recherche ArXiv: '{full_query}' (max {max_results} résultats)")
        
        search = arxiv.Search(
            query=full_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )
        
        documents = []
        for paper in self.client.results(search):
            abstract = paper.summary.replace("\n", " ").strip()
            documents.append({
                "id": f"arxiv_{paper.entry_id.split('/')[-1]}",
                "content": f"{paper.title}\n\n{abstract}",
                "title": paper.title,
                "source": paper.entry_id,
                "domain": "AI",
                "authors": [author.name for author in paper.authors],
                "published": paper.published.isoformat(),
                "categories": paper.categories
            })
        
        print(f"  ✅ {len(documents)} papiers récupérés")
        return documents
    
    def search_by_domain(self, domain: str, max_results: int = None) -> List[Dict]:
        """
        Recherche par domaine spécifique.
        """
        query = f"cat:{domain}"
        return self.fetch_papers(query, max_results)


# === TEST ISOLÉ ===
if __name__ == "__main__":
    print("🧪 Test du service ArXiv...\n")
    
    service = ResearchService(max_results=5)
    
    # Test 1 : Recherche par mot-clé
    print("=" * 60)
    print("📝 Test 1: Recherche 'RAG'")
    print("=" * 60)
    papers = service.fetch_papers("retrieval augmented generation", max_results=3, category="cs.CL")
    
    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}] {paper['title']}")
        print(f"    Auteurs: {', '.join(paper['authors'][:3])}")
        print(f"    Publié: {paper['published'][:10]}")
        print(f"    URL: {paper['source']}")
        print(f"    Résumé: {paper['content'][:150]}...")
    
    print("\n✅ Test terminé !")