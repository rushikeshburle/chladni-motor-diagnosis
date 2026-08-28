"""
Vision-Based Chladni Pattern Analysis for Electric Motor Vibration Fault Diagnosis
Main FastAPI Application
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import uvicorn
import sys
import os

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from backend.api.diagnosis import diagnosis_router
from backend.api.upload import upload_router
from backend.api.history import history_router
from backend.database.database import init_db

# Initialize FastAPI app
app = FastAPI(
    title="Vision-Based Chladni Pattern Analysis",
    description="Electric Motor Vibration Fault Diagnosis System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(diagnosis_router, prefix="/api/diagnosis", tags=["diagnosis"])
app.include_router(upload_router, prefix="/api/upload", tags=["upload"])
app.include_router(history_router, prefix="/api/history", tags=["history"])

# Create necessary directories
UPLOAD_DIR = Path("uploads/temp")
REPORT_DIR = Path("reports")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Vision-Based Chladni Pattern Analysis API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
