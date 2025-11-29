import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api.routes import router as rag_router
from app.logging_config import setup_logging
import logging
from dotenv import load_dotenv


load_dotenv()
setup_logging() 

app = FastAPI(
    title="RAG Based Knowledge Assistant",
    description="API For RAG Based Knowledge Assistant",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logging.getLogger("main").info("FastAPI app started")

app.include_router(rag_router, prefix="/api", tags=["RAG"])

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok", "version": app.version}


@app.get("/")
async def root():
    """Redirect to the API documentation."""
    return {"message": "Welcome to the RAG Pipeline API", "docs_url": "/docs"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
