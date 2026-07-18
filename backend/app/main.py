from fastapi import FastAPI, UploadFile, File, HTTPException
# Create FastAPI application
app = FastAPI(
    title="OmniBrain Backend API",
    description="Backend API for OmniBrain Multi-Modal RAG Project",
    version="1.0.0"
)

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

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
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

    if len(content) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:
        pass
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File uploaded successfully"
    }    
