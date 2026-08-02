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
            raise ValueError("GROQ_API_KEY not found in .env file!")
    
    def generate(self, question: str, context: str) -> str:
        """Generate exact answer from document"""
        
        prompt = f"""Read the text below and answer the question accurately.

TEXT:
{context}

QUESTION: {question}

- Answer using ONLY information from the text above
- Be specific and concise
- If not in text, say "Not found in document"

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
                "max_tokens": 150
            }
            
            response = requests.post(
                self.url,
                json=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                return f"❌ ERROR: {response.text}"
            
            answer = response.json()["choices"][0]["message"]["content"]
            return answer.strip()
        
        except Exception as e:
            return f"❌ ERROR: {str(e)}"