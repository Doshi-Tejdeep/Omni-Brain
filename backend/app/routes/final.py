import os
import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.app.services.vision_service import analyze_image
from backend.app.services.rag_service import generate_answer


router = APIRouter()

logger = logging.getLogger(__name__)

UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/final",
    summary="Final Multimodal API",
    description=(
        "Accepts a question, document ID, and image, "
        "then performs Gemini Vision analysis and optional document RAG."
    ),
    responses={
        200: {"description": "Final API executed successfully"},
        400: {"description": "Invalid request"},
        500: {"description": "Internal Server Error"},
    },
)
async def final_api(
    question: str = Form(...),
    document_id: str = Form(...),
    image: UploadFile = File(...),
):
    try:
        logger.info(
            f"Final API request received: {image.filename}"
        )

        # =========================================================
        # 1. VALIDATE IMAGE
        # =========================================================

        allowed_types = {
            "image/png",
            "image/jpeg",
            "image/jpg",
            "image/webp",
        }

        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Only PNG, JPG, JPEG, and WEBP images are allowed."
                ),
            )

        # =========================================================
        # 2. VALIDATE QUESTION
        # =========================================================

        if not question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )

        # =========================================================
        # 3. VALIDATE DOCUMENT ID
        # =========================================================

        if not document_id.strip():
            raise HTTPException(
                status_code=400,
                detail="Document ID cannot be empty.",
            )

        # =========================================================
        # 4. READ IMAGE
        # =========================================================

        image_bytes = await image.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty.",
            )

        # =========================================================
        # 5. SAVE IMAGE
        # =========================================================

        safe_filename = os.path.basename(
            image.filename or "uploaded_image"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            safe_filename,
        )

        with open(file_path, "wb") as buffer:
            buffer.write(image_bytes)

        saved_size = os.path.getsize(file_path)

        if saved_size == 0:
            raise HTTPException(
                status_code=500,
                detail="Image was saved as an empty file.",
            )

        logger.info(
            f"Image saved at {file_path}"
        )

        # =========================================================
        # 6. GEMINI VISION
        # =========================================================
        # Gemini is called ONLY from /final.
        # /vision does NOT call Gemini or Ollama.

        logger.info(
            "Starting Gemini Vision analysis..."
        )

        vision_analysis = analyze_image(
            image_path=file_path,
            question=question,
        )

        logger.info(
            "Gemini Vision analysis completed."
        )

        # =========================================================
        # 7. OPTIONAL DOCUMENT RAG
        # =========================================================

        rag_result = None

        try:
            logger.info(
                f"Starting document RAG for document: {document_id}"
            )

            rag_result = await generate_answer(
                question,
                document_id,
            )

            logger.info(
                "Document RAG completed."
            )

        except Exception as rag_error:
            logger.warning(
                f"Document RAG skipped: {rag_error}"
            )

        # =========================================================
        # 8. CREATE ONE FINAL ANSWER
        # =========================================================

        final_answer = vision_analysis
        sources = []

        if rag_result:
            rag_answer = rag_result.get("answer", "")
            rag_sources = rag_result.get("sources", [])

            if (
                rag_answer
                and rag_answer.strip()
                and "I could not find the answer" not in rag_answer
            ):
                final_answer = (
                    f"{vision_analysis}\n\n"
                    f"Document information:\n"
                    f"{rag_answer}"
                )

                sources = rag_sources

        # =========================================================
        # 9. RETURN ONE CLEAN RESPONSE
        # =========================================================

        return {
            "message": "Final API executed successfully",
            "question": question,
            "document_id": document_id,
            "image": image.filename,
            "image_path": file_path,
            "image_size": saved_size,
            "answer": final_answer,
            "sources": sources,
            "status": "Multimodal analysis completed successfully",
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            "Final API failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )