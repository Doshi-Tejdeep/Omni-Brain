from fastapi import APIRouter

router = APIRouter()
@router.get(
    "/",
    summary="Root Endpoint",
    description="Returns a welcome message for the OmniBrain Backend API."
)
def read_root():
    return {
        "message": "Welcome to OmniBrain Backend API"
    }

# Health endpoint
@router.get(
    "/health",
    summary="Health Check",
    description="Checks whether the backend server is running properly."
)
def health():
    return {
        "status": "healthy",
        "message": "Backend is running successfully"
    }
