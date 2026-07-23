from fastapi import FastAPI
from app.utils.logger import logger
from app.routes.health import router as health_router
from app.routes.upload import router as upload_router
from app.routes.ask import router as ask_router

import os

app = FastAPI(
    title="OmniBrain Backend API",
    description="Backend API for OmniBrain Multi-Modal RAG Project",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    logger.info("Backend server started")

UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(ask_router)
