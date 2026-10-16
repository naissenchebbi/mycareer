"""
Service d'ingestion : récupère les données externes et les ajoute au RAG
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.research_service import ResearchService
from rag.pipeline import RAGPipeline
from rag.retriever import VectorRetriever


class IngestionService:
    """Service pour ingérer les données externes dans le RAG"""
    
    def __init__(self, pipeline: RAGPipeline):
        self.pipeline = pipeline
        self.research = ResearchService(max_results=10)
    
    def clear_database(self):
        """Vide la base ChromaDB"""
        print("🗑️ Nettoyage de la base...")
        retriever = self.pipeline.retriever
        retriever.client.delete_collection(retriever.collection.name)
        retriever.collection = retriever.client.get_or_create_collection(
            name=retriever.collection.name,
            metadata={"hnsw:space": "cosine"}
        )
        print("  ✅ Base nettoyée")
    
    def ingest_arxiv(self, query: str, category: str = "cs.CL", max_results: int = 5):
        """Récupère et ajoute des papiers ArXiv au RAG"""
        print(f"📥 Ingestion ArXiv: '{query}' (catégorie: {category})")
        
        papers = self.research.fetch_papers(query, max_results, category)
        
        if papers:
            self.pipeline.add_documents(papers)
            print(f"  ✅ {len(papers)} papiers ajoutés au RAG")
        else:
            print(f"  ⚠️ Aucun papier trouvé")
        
        return len(papers)


# === TEST ISOLÉ ===
if __name__ == "__main__":
    print("🧪 Test du service d'ingestion...\n")
    print("=" * 60)
    
    # 1. Créer le pipeline
    pipeline = RAGPipeline()
    
    # 2. Créer le service d'ingestion
    ingestion = IngestionService(pipeline)
    
    # 3. NETTOYER la base (important !)
    ingestion.clear_database()
    
    # 4. Ingérer des papiers ArXiv
    print("\n" + "=" * 60)
    print("📥 INGESTION ARXIV")
    print("=" * 60)
    ingestion.ingest_arxiv("retrieval augmented generation", category="cs.CL", max_results=5)
    
    # 5. Tester une requête ciblée
    print("\n" + "=" * 60)
    print("❓ TEST: Liste les papiers sur le RAG")
    print("=" * 60)
    
    result = pipeline.query("Liste les papiers sur le RAG", top_k=5)
    print(f"\n💬 Réponse:\n{result['answer']}\n")
    print(f"📚 Sources:")
    for src in result['sources']:
        print(f"  [{src['id']}] {src['title'][:70]}...")
        print(f"      Source: {src['source']}")
        print(f"      Score: {src['score']}")
    
    print("\n✅ Test terminé !")