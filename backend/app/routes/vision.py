from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.utils.logger import logger
from backend.app.config import UPLOAD_DIR
import os
import shutil

router = APIRouter()

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/vision",
    summary="Vision API",
    description="Uploads an image for vision processing.",
    responses={
        200: {"description": "Image uploaded successfully"},
        400: {"description": "Invalid image"},
        500: {"description": "Internal Server Error"},
    },
)
async def vision_api(file: UploadFile = File(...)):
    try:
        logger.info(f"Vision request received: {file.filename}")

        allowed_types = ["image/png", "image/jpeg", "image/jpg"]

        if file.content_type not in allowed_types:
            logger.warning(f"Invalid image uploaded: {file.filename}")

            raise HTTPException(
                status_code=400, detail="Only PNG and JPG images are allowed."
            )

        content = await file.read()

        if len(content) == 0:
            logger.warning(f"Empty image uploaded: {file.filename}")

            raise HTTPException(status_code=400, detail="Uploaded image is empty.")

        await file.seek(0)

        safe_filename = os.path.basename(file.filename)

        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Image stored at {file_path}")

        return {
            "message": "Image uploaded successfully",
            "filename": file.filename,
            "content_type": file.content_type,
            "path": file_path,
            "vision_status": "Vision processing is under development.",
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Vision API failed: {str(e)}")

        raise HTTPException(status_code=500, detail="Internal Server Error")
