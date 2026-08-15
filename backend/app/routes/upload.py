from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.document_processing.index_document import index_document
from backend.app.utils.logger import logger
from backend.app.config import (
    MAX_FILE_SIZE,
    ALLOWED_FILE_TYPES,
    UPLOAD_DIR,
)
import os
import shutil

router = APIRouter()

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/upload",
    summary="Upload PDF",
    description="Uploads a PDF file.",
    responses={
        200: {"description": "File uploaded successfully"},
        400: {"description": "Invalid upload request"},
        500: {"description": "Internal Server Error"},
    },
)
async def upload_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Upload request received: {file.filename}")

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Invalid filename.")

        if file.content_type not in ALLOWED_FILE_TYPES:
            logger.warning(f"Invalid file uploaded: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )

        content = await file.read()

        if len(content) == 0:
            logger.warning(f"Empty file uploaded: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        if len(content) > MAX_FILE_SIZE:
            logger.warning(f"File too large: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="File size exceeds 10MB.",
            )

        await file.seek(0)

        safe_filename = os.path.basename(file.filename)
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"{file.filename} stored at {file_path}")

        logger.info("Indexing uploaded document...")

        document_id = index_document(file_path)

        logger.info("Document indexed successfully.")

        logger.info(f"{file.filename} uploaded successfully")
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "content_type": file.content_type,
            "path": file_path,
            "document_id": document_id,
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Upload failed")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )
