import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Charger .env depuis la racine du projet (robuste)
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class GroqGenerator:
    """Générateur de réponses via Groq LLM"""
    
    def __init__(self, model: str = "openai/gpt-oss-20b"):
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ GROQ_API_KEY manquante dans .env")
        
        if not self.api_key.startswith("gsk_"):
            raise ValueError("❌ GROQ_API_KEY invalide (doit commencer par gsk_)")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Génère une réponse via Groq"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content
        
        except Exception as e:
            return f"❌ Erreur Groq: {str(e)}"


# === TEST ISOLÉ ===
if __name__ == "__main__":
    print("🧪 Test du générateur Groq...\n")
    
    try:
        gen = GroqGenerator()
        
        # Test 1 : Question simple
        print("📝 Test 1: Question simple")
        response = gen.generate("Explique en une phrase ce qu'est le RAG.")
        print(f"Réponse: {response}\n")
        
        # Test 2 : Avec system prompt
        print("📝 Test 2: Avec system prompt")
        response = gen.generate(
            prompt="Quelles sont les news en IA ?",
            system_prompt="Tu es un assistant spécialisé en veille technologique. Réponds de manière concise."
        )
        print(f"Réponse: {response}\n")
        
        print("✅ Tous les tests passés !")
        
    except ValueError as e:
        print(f"❌ Erreur de configuration: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")