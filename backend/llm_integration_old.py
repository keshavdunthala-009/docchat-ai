import requests
import os
from dotenv import load_dotenv

load_dotenv()

class LLMIntegration:
    """Simple LLM integration without conflicts"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in .env")
    
    def generate_answer(self, question: str, context: str) -> str:
        """Generate answer using OpenAI API"""
        
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are helpful. Answer based ONLY on provided context. If answer not in context, say 'I don't have this information.'"
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"OpenAI API error: {response.text}")
        
        return response.json()["choices"][0]["message"]["content"]

# Test
if __name__ == "__main__":
    llm = LLMIntegration()
    
    context = "Python is a programming language. It's used for web development and AI."
    question = "What is Python used for?"
    
    answer = llm.generate_answer(question, context)
    print(f"Q: {question}")
    print(f"A: {answer}")