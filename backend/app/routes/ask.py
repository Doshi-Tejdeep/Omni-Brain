from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.logger import logger

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
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
