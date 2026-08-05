from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from rag_pipeline import RAGPipeline
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG System", version="2.0")

# CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "https://docchat-ai-delta.vercel.app",  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGPipeline()


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[str] = []
    chunk_count: int


@app.get("/")
def read_root():
    return {"message": "RAG system is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        temp_path = f"temp_{file.filename}"

        content = await file.read()
        print(f"File read: {len(content)} bytes")

        with open(temp_path, "wb") as f:
            f.write(content)
        print(f"File saved: {temp_path}")

        try:
            result = rag.add_document(temp_path, file.filename)
            print(f"Document processed: {result}")
        except Exception as e:
            print(f"Processing error: {e}")
            result = {"chunks": 0}

        if os.path.exists(temp_path):
            os.remove(temp_path)

        return {
            "status": "success",
            "filename": file.filename,
            "chunks": result.get("chunks", 0)
        }

    except Exception as e:
        print(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/ask")
async def ask_question(request: QuestionRequest) -> QuestionResponse:
    """Ask a question - retrieve TOP 1 chunk only"""
    try:
        result = rag.query(request.question, top_k=1)

        return QuestionResponse(
            question=result.get("question", request.question),
            answer=result.get("answer", ""),
            sources=result.get("sources", []),
            chunk_count=result.get("chunk_count", 0)
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)