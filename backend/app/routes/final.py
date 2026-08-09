from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.app.utils.logger import logger
from backend.app.services.rag_service import generate_answer
import os
import shutil


router = APIRouter()

UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/final",
    summary="Final API",
    description="Accepts a question and an image.",
)
async def final_api(
    question: str = Form(...),
    image: UploadFile = File(...),
):
    try:
        logger.info(f"Final API request received: {image.filename}")

        allowed_types = [
            "image/png",
            "image/jpeg",
            "image/jpg",
        ]

        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Only PNG and JPG images are allowed.",
            )

        content = await image.read()

        if len(content) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty.",
            )

        await image.seek(0)

        safe_filename = os.path.basename(image.filename)
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        logger.info(f"Image stored at {file_path}")

        answer = await generate_answer(question)

        return {
            "message": "Final API executed successfully",
            "question": question,
            "image": image.filename,
            "answer": answer,
            "status": "Final API working",
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Final API failed: {e}")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )
