from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.base import Base
from app.database.connection import engine
from app.api.routes import health, patients, ai

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MediPredict AI",
    description="Patient record management with AI-generated informational remarks",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(patients.router)
app.include_router(ai.router)


@app.get("/")
async def root():
    return {
        "message": "MediPredict AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }
