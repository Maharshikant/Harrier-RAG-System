"""
Tata Harrier BS6 Multimodal RAG System
FastAPI application entry point.
"""

from fastapi import FastAPI
from src.api.routes import router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Tata Harrier BS6 RAG System",
    description=(
        "Multimodal Retrieval-Augmented Generation system "
        "for Tata Harrier BS6 service manual intelligence. "
        "Supports text, table, and image-based queries."
    ),
    version="1.0.0",
    contact={
        "name": "Harrier RAG API",
    }
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Tata Harrier BS6 RAG System is running.",
        "docs": "/docs",
        "health": "/health"
    }