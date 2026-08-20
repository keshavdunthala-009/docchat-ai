import requests
import os
import re
import time
from dotenv import load_dotenv

load_dotenv()


class AnswerGenerator:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
        self.url = f"{self.base_url}/chat/completions"
        # Falls back to a working default; override with GROQ_MODEL if you want
        self.model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found!")

    def list_models(self) -> list:
        """Return every model ID your API key can access."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(
            f"{self.base_url}/models",
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        return [m["id"] for m in response.json().get("data", [])]

    def generate(self, question: str, context: str, max_context_chars: int = 12000) -> str:
        # Trim oversized context to conserve free-tier tokens
        if len(context) > max_context_chars:
            context = context[:max_context_chars]

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

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 500
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.url,
                    json=data,
                    headers=headers,
                    timeout=30
                )

                # Rate limited — wait and retry (common on free tier)
                if response.status_code == 429:
                    retry_after = response.headers.get("retry-after")
                    wait = float(retry_after) if retry_after else (2 ** attempt)
                    if attempt < max_retries - 1:
                        time.sleep(wait)
                        continue
                    return f"ERROR: rate limited, retries exhausted. Wait ~{wait}s and try again."

                if response.status_code != 200:
                    # If the model itself is invalid, show the valid options
                    if "model_not_found" in response.text:
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

            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return f"ERROR: {str(e)}"

        return "ERROR: unexpected failure"


if __name__ == "__main__":
    gen = AnswerGenerator()
    print("Models available to your key:")
    for model_id in gen.list_models():
        print(f"  - {model_id}")