from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG System", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import after app creation
from rag_pipeline import RAGPipeline, document_store

rag_sessions = {}

def get_rag(session_id: str) -> RAGPipeline:
    if session_id not in rag_sessions:
        rag_sessions[session_id] = RAGPipeline(session_id=session_id)
    return rag_sessions[session_id]

class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default"

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
    return {"status": "ok", "sessions": list(document_store.keys())}

@app.get("/session")
def create_session():
    session_id = str(uuid.uuid4())
    return {"session_id": session_id}

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    session_id: str = "default"
):
    try:
        print(f"UPLOAD - Session: {session_id}, File: {file.filename}")

        temp_path = f"temp_{session_id}_{file.filename}"
        content = await file.read()

        with open(temp_path, "wb") as f:
            f.write(content)

        rag = get_rag(session_id)
        result = rag.add_document(temp_path, file.filename)

        if os.path.exists(temp_path):
            os.remove(temp_path)

        print(f"UPLOAD SUCCESS - Session: {session_id}")
        print(f"Document store keys: {list(document_store.keys())}")

        return {
            "status": "success",
            "filename": file.filename,
            "chunks": result.get("chunks", 0),
            "session_id": session_id
        }

    except Exception as e:
        print(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ask")
async def ask_question(request: QuestionRequest) -> QuestionResponse:
    try:
        print(f"ASK - Session: {request.session_id}")
        print(f"Document store keys: {list(document_store.keys())}")

        rag = get_rag(request.session_id)
        result = rag.query(request.question)

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