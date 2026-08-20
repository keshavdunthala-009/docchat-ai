import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()


class AnswerGenerator:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
        self.url = f"{self.base_url}/chat/completions"
        # Override via GROQ_MODEL in your .env; falls back to a known-good default
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found!")

    def list_models(self) -> list[str]:
        """Return every model ID your API key can access."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(
            f"{self.base_url}/models",
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        return [m["id"] for m in response.json().get("data", [])]

    def generate(self, question: str, context: str) -> str:

        prompt = f"""You are analyzing a document. Answer ONLY based on the document text below.

DOCUMENT TEXT:
{context}

QUESTION: {question}

STRICT RULES:
- Answer ONLY what is explicitly written in the document
- For NAME: Look at the very beginning of the document
- For PROJECTS: List ONLY items under PROJECTS heading
- For SKILLS: List ALL skills including soft and technical skills
- For EXPERIENCE: List work experience details
- For EDUCATION: List education details
- For CERTIFICATIONS: List all certifications
- Be specific with names, dates, numbers
- If not found say "Not mentioned in document"

ANSWER:"""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 500
            }

            response = requests.post(
                self.url,
                json=data,
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:
                # If the model is the problem, surface the valid options
                if response.status_code == 404 or "model" in response.text.lower():
                    try:
                        available = ", ".join(self.list_models())
                        return (
                            f"ERROR: model '{self.model}' not available. "
                            f"Set GROQ_MODEL to one of: {available}"
                        )
                    except Exception:
                        pass
                return f"ERROR: {response.text}"

            answer = response.json()["choices"][0]["message"]["content"]

            # Remove thinking tags if present
            answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL).strip()

            return answer.strip()

        except Exception as e:
            return f"ERROR: {str(e)}"


if __name__ == "__main__":
    gen = AnswerGenerator()
    print("Models available to your key:")
    for model_id in gen.list_models():
        print(f"  - {model_id}")