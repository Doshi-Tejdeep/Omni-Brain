from fastapi import FastAPI, UploadFile, File

# Create FastAPI application
app = FastAPI(
    title="OmniBrain Backend API",
    description="Backend API for OmniBrain Multi-Modal RAG Project",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
def root():
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
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File uploaded successfully"
    }
