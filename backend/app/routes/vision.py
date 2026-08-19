import os
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.config import UPLOAD_DIR
from backend.app.utils.logger import logger


router = APIRouter()

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/vision",
    summary="Vision Image Upload",
    description="Uploads an image for later multimodal processing. Gemini analysis is performed only by /final.",
    responses={
        200: {"description": "Image uploaded successfully"},
        400: {"description": "Invalid image"},
        500: {"description": "Internal Server Error"},
    },
)
async def vision_api(file: UploadFile = File(...)):
    try:
        logger.info(
            f"Vision image upload received: {file.filename}"
        )

        # ---------------------------------------------------------
        # 1. Validate image
        # ---------------------------------------------------------

        allowed_types = {
            "image/png",
            "image/jpeg",
            "image/jpg",
            "image/webp",
        }

        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Only PNG, JPG, JPEG, and WEBP "
                    "images are allowed."
                ),
            )

        # ---------------------------------------------------------
        # 2. Read image
        # ---------------------------------------------------------

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty.",
            )

        # ---------------------------------------------------------
        # 3. Safe filename
        # ---------------------------------------------------------

        safe_filename = os.path.basename(
            file.filename or "uploaded_image"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            safe_filename,
        )

        # ---------------------------------------------------------
        # 4. Save image
        # ---------------------------------------------------------

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        image_id = str(uuid.uuid4())

        logger.info(
            f"Image saved successfully: "
            f"{file_path} ({len(content)} bytes)"
        )

        # ---------------------------------------------------------
        # IMPORTANT:
        # Do NOT call Gemini here.
        # Do NOT call Ollama here.
        # ---------------------------------------------------------

        return {
            "message": "Image uploaded successfully",
            "filename": file.filename,
            "content_type": file.content_type,
            "path": file_path,
            "size_bytes": len(content),
            "image_id": image_id,
            "vision_status": (
                "Image saved successfully. "
                "Gemini analysis will be performed by /final."
            ),
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Vision image upload failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )