from fastapi import FastAPI, UploadFile, File, HTTPException
from app.utils.logger import logger
# Create FastAPI application
app = FastAPI(
    title="OmniBrain Backend API",
    description="Backend API for OmniBrain Multi-Modal RAG Project",
    version="1.0.0"
)
@app.on_event("startup")
async def startup_event():
    logger.info("Backend server started")

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to OmniBrain Backend API"
    }

# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "Backend is running successfully"
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    logger.info(f"Upload request received: {file.filename}")
    if file.content_type != "application/pdf":
        logger.warning(
    f"Invalid file uploaded: {file.filename}"
)
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    content = await file.read()
    logger.info(
    f"{file.filename} uploaded successfully"
)

    MAX_SIZE = 10 * 1024 * 1024

    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10MB."
        )

    await file.seek(0)

    if len(content) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:
        pass
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File uploaded successfully"
    }   
