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
        """Generate accurate answer from document"""
        
        prompt = f"""You are a document analysis expert. Read the document text carefully and answer the question accurately.

DOCUMENT TEXT:
{context}

QUESTION: {question}

INSTRUCTIONS:
- Read ALL the text carefully
- Answer ONLY based on information in the document
- List ALL relevant items found
- Be specific with names, dates, and details
- If listing projects/skills/experience, include ALL of them
- Keep answer clear and concise

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
                "max_tokens": 300
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