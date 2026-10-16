"""
Pipeline RAG complet pour MyCareer
Combine : Embedding + Retriever + Generator
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

# Ajouter le dossier backend au path pour les imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag.embedding import EmbeddingService
from rag.retriever import VectorRetriever
from rag.generator import GroqGenerator


class RAGPipeline:
    """
    Pipeline RAG complet :
    1. Recherche les documents pertinents (Retrieval)
    2. Augmente le prompt avec le contexte (Augmentation)
    3. Génère une réponse avec le LLM (Generation)
    """
    
    def __init__(self):
        print("🔄 Initialisation du pipeline RAG...")
        self.embedder = EmbeddingService()
        self.retriever = VectorRetriever()
        self.generator = GroqGenerator()
        print("✅ Pipeline RAG prêt !\n")
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Ajoute des documents à la base de connaissances.
        
        Args:
            documents: Liste de dicts avec 'content', 'title', 'source', 'domain'
        """
        self.retriever.add_documents(documents)
    
    def query(
        self,
        question: str,
        top_k: int = 3,
        domain: str = None,
        language: str = "fr"
    ) -> Dict[str, Any]:
        """
        Exécute le pipeline RAG complet.
        
        Args:
            question: Question de l'utilisateur
            top_k: Nombre de documents à récupérer
            domain: Filtrer par domaine (optionnel)
            language: Langue de réponse (fr, en, ar)
        
        Returns:
            Dict avec 'answer', 'sources', 'context'
        """
        print(f"🔍 Recherche pour: {question}")
        
        # === ÉTAPE 1 : RETRIEVAL ===
        retrieved_docs = self.retriever.search(
            query=question,
            top_k=top_k,
            domain=domain
        )
        
        if not retrieved_docs:
            return {
                "answer": "Je n'ai pas trouvé d'informations pertinentes dans ma base de connaissances.",
                "sources": [],
                "context": []
            }
        
        print(f"  ✅ {len(retrieved_docs)} documents trouvés")
        
        # === ÉTAPE 2 : AUGMENTATION ===
        context_parts = []
        for i, doc in enumerate(retrieved_docs):
            title = doc["metadata"].get("title", f"Document {i+1}")
            content = doc["content"]
            context_parts.append(f"[Source {i+1}: {title}]\n{content}")
        
        context = "\n\n".join(context_parts)
        
        # === ÉTAPE 3 : GENERATION ===
        system_prompt = f"""Tu es MyCareer, un assistant IA spécialisé dans la veille technologique.

RÈGLES IMPORTANTES:
1. Réponds UNIQUEMENT en te basant sur le contexte fourni ci-dessous.
2. Si l'information n'est pas dans le contexte, dis-le clairement.
3. Cite tes sources en utilisant [Source N] dans ta réponse.
4. Réponds en {language} de manière claire et structurée.
5. Ne jamais inventer d'informations.

CONTEXTE:
{context}
"""
        
        print("  🤖 Génération de la réponse...")
        answer = self.generator.generate(
            prompt=question,
            system_prompt=system_prompt
        )
        
        # === FORMATAGE DES SOURCES ===
        sources = []
        for i, doc in enumerate(retrieved_docs):
            sources.append({
                "id": i + 1,
                "title": doc["metadata"].get("title", f"Source {i+1}"),
                "source": doc["metadata"].get("source", ""),
                "domain": doc["metadata"].get("domain", ""),
                "score": round(doc.get("score", 0), 4),
                "preview": doc["content"][:150] + "..."
            })
        
        return {
            "answer": answer,
            "sources": sources,
            "context": [doc["content"] for doc in retrieved_docs]
        }


# === TEST ISOLÉ ===
if __name__ == "__main__":
    print("🧪 Test du pipeline RAG complet...\n")
    print("=" * 60)
    
    # 1. Initialiser le pipeline
    pipeline = RAGPipeline()
    
    # 2. Ajouter des documents de test
    print("📝 Ajout de documents de test...")
    test_docs = [
        {
            "id": "doc_rag_1",
            "content": "Le RAG (Retrieval-Augmented Generation) est une technique d'IA qui combine la recherche d'informations dans une base de connaissances avec la génération de texte par un modèle de langage. Cette approche permet de réduire les hallucinations des LLM et de fournir des réponses basées sur des sources vérifiables.",
            "title": "Introduction au RAG",
            "source": "arxiv.org",
            "domain": "AI"
        },
        {
            "id": "doc_rag_2",
            "content": "Le pipeline RAG se compose de trois étapes principales : le Retrieval (recherche des documents pertinents), l'Augmentation (injection du contexte dans le prompt), et la Generation (production de la réponse par le LLM).",
            "title": "Architecture RAG",
            "source": "huggingface.co",
            "domain": "AI"
        },
        {
            "id": "doc_fastapi_1",
            "content": "FastAPI est un framework web Python moderne et rapide pour créer des API REST. Il utilise les annotations de type Python et Pydantic pour la validation des données. FastAPI supporte nativement l'asynchrone avec async/await.",
            "title": "Guide FastAPI",
            "source": "fastapi.tiangolo.com",
            "domain": "Web"
        },
        {
            "id": "doc_chroma_1",
            "content": "ChromaDB est une base de données vectorielle open-source conçue pour la recherche sémantique. Elle stocke les embeddings et permet de rechercher les documents les plus similaires à une requête donnée.",
            "title": "ChromaDB Documentation",
            "source": "trychroma.com",
            "domain": "AI"
        },
        {
            "id": "doc_groq_1",
            "content": "Groq est une plateforme d'inférence ultra-rapide pour les LLM. Elle utilise des puces LPU (Language Processing Units) spécialement conçues pour accélérer les modèles de langage. Groq propose une API gratuite compatible avec OpenAI.",
            "title": "Groq Platform",
            "source": "groq.com",
            "domain": "AI"
        }
    ]
    
    pipeline.add_documents(test_docs)
    print(f"  ✅ {len(test_docs)} documents ajoutés\n")
    
    # 3. Tester le pipeline avec plusieurs questions
    print("=" * 60)
    print("📝 Test du pipeline RAG avec questions\n")
    
    test_questions = [
        "Qu'est-ce que le RAG ?",
        "Comment fonctionne FastAPI ?",
        "Qu'est-ce que ChromaDB ?",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"❓ Question {i}: {question}")
        print("=" * 60)
        
        result = pipeline.query(question, top_k=3)
        
        print(f"\n💬 Réponse:\n{result['answer']}\n")
        
        print(f"📚 Sources utilisées:")
        for src in result['sources']:
            print(f"  [{src['id']}] {src['title']} (score: {src['score']})")
            print(f"      → {src['source']}")
    
    print("\n" + "=" * 60)
    print("✅ Tous les tests passés !")
    print("=" * 60)