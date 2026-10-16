import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from pathlib import Path

# Import de l'EmbeddingService
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from rag.embedding import EmbeddingService


class VectorRetriever:
    """Retriever vectoriel via ChromaDB"""
    
    def __init__(self, collection_name: str = "mycareer_knowledge", persist_dir: str = "./chroma_db"):
        self.embedding_service = EmbeddingService()
        
        # Client ChromaDB avec persistance
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Créer ou récupérer la collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Ajoute des documents à la base"""
        ids = []
        texts = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            ids.append(doc.get("id", f"doc_{i}"))
            texts.append(doc["content"])
            metadatas.append({
                "title": doc.get("title", ""),
                "source": doc.get("source", ""),
                "domain": doc.get("domain", "general")
            })
        
        # Générer les embeddings
        embeddings = self.embedding_service.encode(texts)
        
        # Ajouter à ChromaDB
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )
    
    def search(self, query: str, top_k: int = 3, domain: str = None) -> List[Dict]:
        """Recherche sémantique"""
        query_embedding = self.embedding_service.encode_query(query)
        
        where_filter = {"domain": domain} if domain else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where=where_filter
        )
        
        documents = []
        if results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                documents.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i],
                    "score": 1 - results['distances'][0][i]
                })
        
        return documents


# === TEST ISOLÉ ===
if __name__ == "__main__":
    print("🧪 Test du retriever ChromaDB...\n")
    
    retriever = VectorRetriever()
    
    # 1. Ajouter des documents
    print("📝 Test 1: Ajout de documents")
    docs = [
        {
            "id": "doc_1",
            "content": "Le RAG (Retrieval-Augmented Generation) combine la recherche d'informations avec la génération de texte par un LLM.",
            "title": "Introduction au RAG",
            "source": "arxiv.org",
            "domain": "AI"
        },
        {
            "id": "doc_2",
            "content": "FastAPI est un framework web Python moderne pour créer des API REST avec async/await.",
            "title": "Guide FastAPI",
            "source": "fastapi.tiangolo.com",
            "domain": "Web"
        },
        {
            "id": "doc_3",
            "content": "ChromaDB est une base de données vectorielle open-source pour la recherche sémantique.",
            "title": "ChromaDB Docs",
            "source": "trychroma.com",
            "domain": "AI"
        },
    ]
    retriever.add_documents(docs)
    print(f"  ✅ {len(docs)} documents ajoutés\n")
    
    # 2. Rechercher
    print("📝 Test 2: Recherche sémantique")
    queries = [
        "Qu'est-ce que le RAG ?",
        "Comment créer une API en Python ?",
        "Base de données vectorielle",
    ]
    
    for query in queries:
        print(f"\n  🔍 Query: {query}")
        results = retriever.search(query, top_k=2)
        for i, r in enumerate(results):
            print(f"    [{r['score']:.4f}] {r['metadata']['title']}")
            print(f"      → {r['content'][:80]}...")
    
    print("\n✅ Tous les tests passés !")