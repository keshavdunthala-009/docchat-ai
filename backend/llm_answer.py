import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()


class AnswerGenerator:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found!")

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
                return f"ERROR: {response.text}"

            answer = response.json()["choices"][0]["message"]["content"]

            # Remove thinking tags if present
            answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL).strip()

            return answer.strip()

        except Exception as e:
            return f"ERROR: {str(e)}"