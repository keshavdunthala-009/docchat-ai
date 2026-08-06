import requests
import os
from dotenv import load_dotenv

load_dotenv()


class AnswerGenerator:
    """Generate accurate answers using Groq API"""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found!")

    def generate(self, question: str, context: str) -> str:

        prompt = f"""You are analyzing a resume/document. Answer ONLY based on the document text below.

DOCUMENT TEXT:
{context}

QUESTION: {question}

STRICT RULES:
- Answer ONLY what is explicitly written in the document
- For projects question: List ONLY items under PROJECTS heading
- Do NOT include internship duties, volunteering, or certifications as projects
- Include project names, dates, and key achievements
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
                return f"ERROR: {response.text}"

            answer = response.json()["choices"][0]["message"]["content"]
            return answer.strip()

        except Exception as e:
            return f"ERROR: {str(e)}"