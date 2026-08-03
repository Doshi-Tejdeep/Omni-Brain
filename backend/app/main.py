from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.utils.logger import logger
from backend.app.routes.health import router as health_router
from backend.app.routes.upload import router as upload_router
from backend.app.routes.ask import router as ask_router
from backend.app.routes.vision import router as vision_router
from backend.app.routes.final import router as final_router
from backend.app.config import UPLOAD_DIR
import os


# Create FastAPI application
app = FastAPI(
    title="OmniBrain Backend API",
    description="Backend API for the OmniBrain Multi-Modal RAG Project.",
    version="1.0.0",
    contact={
        "name": "OmniBrain Backend Team"
    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup_event():
    logger.info("Backend server started")


os.makedirs(UPLOAD_DIR, exist_ok=True)
app.include_router(health_router)
app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(vision_router)
app.include_router(final_router)




