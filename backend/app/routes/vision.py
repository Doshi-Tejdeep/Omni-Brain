from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.utils.logger import logger
from backend.app.config import UPLOAD_DIR

import os
import ollama


router = APIRouter()

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ollama vision model
VISION_MODEL = "gemma3"


@router.post(
    "/vision",
    summary="Vision API",
    description="Uploads an image and analyzes it using a vision model.",
    responses={
        200: {"description": "Image analyzed successfully"},
        400: {"description": "Invalid image"},
        500: {"description": "Internal Server Error"},
    },
)
async def vision_api(file: UploadFile = File(...)):
    try:
        logger.info(f"Vision request received: {file.filename}")

        # ---------------------------------------------------------
        # 1. Validate image type
        # ---------------------------------------------------------
        allowed_types = [
            "image/png",
            "image/jpeg",
            "image/jpg",
        ]

        if file.content_type not in allowed_types:
            logger.warning(
                f"Invalid image uploaded: {file.filename}"
            )

            raise HTTPException(
                status_code=400,
                detail="Only PNG and JPG images are allowed.",
            )

        # ---------------------------------------------------------
        # 2. Read image
        # ---------------------------------------------------------
        content = await file.read()

        if len(content) == 0:
            logger.warning(
                f"Empty image uploaded: {file.filename}"
            )

            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty.",
            )

        # ---------------------------------------------------------
        # 3. Create safe filename
        # ---------------------------------------------------------
        safe_filename = os.path.basename(file.filename)

        file_path = os.path.join(
            UPLOAD_DIR,
            safe_filename,
        )

        # ---------------------------------------------------------
        # 4. Save image
        # ---------------------------------------------------------
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        logger.info(
            f"Image stored at {file_path}"
        )

        # ---------------------------------------------------------
        # 5. Send image to Ollama / Gemma 3
        # ---------------------------------------------------------
        logger.info(
            f"Sending image to Ollama using {VISION_MODEL}"
        )

        response = ollama.chat(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Analyze this image carefully. "
                        "Describe what is visible in the image. "
                        "If there is text, read and explain the important text. "
                        "If it is a screenshot, explain what the screenshot shows. "
                        "Be accurate and concise."
                    ),
                    "images": [file_path],
                }
            ],
        )

        # ---------------------------------------------------------
        # 6. Extract model response
        # ---------------------------------------------------------
        analysis = response["message"]["content"]

        logger.info(
            f"Vision analysis completed for {file.filename}"
        )

        # ---------------------------------------------------------
        # 7. Return response
        # ---------------------------------------------------------
        return {
            "message": "Image analyzed successfully",
            "filename": file.filename,
            "content_type": file.content_type,
            "path": file_path,
            "vision_model": VISION_MODEL,
            "analysis": analysis,
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            f"Vision API failed: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Vision processing failed: {str(e)}",
        )