
from fastapi import FastAPI

from backend.app.api.routes.documents import router as documents_router
from backend.app.api.routes.questions import router as questions_router

app = FastAPI(
    title="DocuMind AI",
    description="AI-powered Document Question Answering System using RAG",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to DocuMind AI!",
        "status": "Application is running"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "application": "DocuMind AI"
    }


app.include_router(documents_router)
app.include_router(questions_router)
