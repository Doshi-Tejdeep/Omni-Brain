from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.utils.logger import logger
import os
import shutil
class QuestionRequest(BaseModel):
    question: str

# Create FastAPI application
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

# Upload endpoint
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
    


    MAX_SIZE = 10 * 1024 * 1024

    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10MB."
        )

    await file.seek(0)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
     shutil.copyfileobj(file.file, buffer)
     logger.info(f"{file.filename} stored at {file_path}")
     logger.info(f"{file.filename} uploaded successfully")


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
    "message": "File uploaded successfully",
    "filename": file.filename,
    "content_type": file.content_type,
    "path": file_path
}

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        
        if not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        
        logger.info(f"Question received: {request.question}")

        
        return {
            "question": request.question,
            "answer": "Answer generation is under development."
        }

    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Ask API failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
