from fastapi import FastAPI

app = FastAPI(title="RAG System", version="1.0")

@app.get("/")
def read_root():
    return {"message": "RAG system is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)