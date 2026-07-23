from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {
        "message": "Welcome to OmniBrain Backend API"
    }

@router.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "Backend is running successfully"
    }
