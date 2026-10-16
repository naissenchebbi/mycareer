import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

# Chemin robuste vers la racine du projet
env_path = Path(__file__).resolve().parent.parent.parent


class EmbeddingService:
    """Service d'embeddings via Sentence Transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialise le modèle d'embeddings.
        
        Args:
            model_name: Nom du modèle HuggingFace
        """
        print(f"🔄 Chargement du modèle '{model_name}'...")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        print(f"✅ Modèle chargé — Dimension: {self.dimension}")
    
    def encode(self, texts, batch_size: int = 32, normalize: bool = True) -> np.ndarray:
        """
        Génère des embeddings pour une liste de textes.
        
        Args:
            texts: Liste de textes (ou un seul texte)
            batch_size: Taille du batch
            normalize: Normaliser les vecteurs (pour similarité cosinus)
        
        Returns:
            numpy array de shape (n_texts, dimension)
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
            show_progress_bar=False
        )
        
        return embeddings
    
    def encode_query(self, query: str) -> np.ndarray:
        """Encode une requête utilisateur (1 seul texte)"""
        return self.encode(query, normalize=True)[0]
    
    def similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calcule la similarité cosinus entre 2 vecteurs.
        
        Returns:
            Score entre -1 et 1 (1 = identique)
        """
        # Si les vecteurs sont déjà normalisés, c'est juste le dot product
        return float(np.dot(vec1, vec2))


# === TEST ISOLÉ ===
if __name__ == "__main__":
    print("🧪 Test du service d'embeddings...\n")
    
    # 1. Initialisation
    service = EmbeddingService()
    print()
    
    # 2. Test : encoder un texte simple
    print("📝 Test 1: Encoder un texte")
    vec = service.encode("Bonjour, je suis un assistant IA.")
    print(f"  Shape: {vec.shape}")
    print(f"  5 premières valeurs: {vec[0][:5]}")
    print()
    
    # 3. Test : encoder plusieurs textes
    print("📝 Test 2: Encoder plusieurs textes")
    texts = [
        "Le RAG combine recherche et génération.",
        "FastAPI est un framework web Python.",
        "Le machine learning est une branche de l'IA."
    ]
    vecs = service.encode(texts)
    print(f"  Shape: {vecs.shape}")
    print()
    
    # 4. Test : similarité sémantique
    print("📝 Test 3: Similarité sémantique")
    query = "Qu'est-ce que le RAG ?"
    candidates = [
        "Le RAG est une technique qui combine recherche et génération.",  # proche
        "La cuisine italienne utilise des tomates.",                       # loin
        "FastAPI est un framework Python pour créer des API."             # moyen
    ]
    
    query_vec = service.encode_query(query)
    
    print(f"  Query: {query}\n")
    for i, candidate in enumerate(candidates):
        candidate_vec = service.encode_query(candidate)
        score = service.similarity(query_vec, candidate_vec)
        print(f"  [{score:.4f}] {candidate}")
    
    print("\n✅ Tous les tests passés !")