from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.logger import logger
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Upload request received: {file.filename}")

        if file.content_type != "application/pdf":
            logger.warning(f"Invalid file uploaded: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        content = await file.read()

        if len(content) == 0:
            logger.warning(f"Empty file uploaded: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        MAX_SIZE = 10 * 1024 * 1024

        if len(content) > MAX_SIZE:
            logger.warning(f"File too large: {file.filename}")
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

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "content_type": file.content_type,
            "path": file_path
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
