from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.app.utils.logger import logger
from backend.app.services.rag_service import generate_answer
import os
import shutil
router = APIRouter()
UPLOAD_DIR = "storage/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)
@router.post(
    "/final",
    summary="Final API",
    description="Accepts a question and an image."
)
async def final_api(
    question: str = Form(...),
    image: UploadFile = File(...)
):
    try:
                logger.info(f"Final API request received: {image.filename}")

                allowed_types = [
                 "image/png",
                 "image/jpeg",
                 "image/jpg"
        ]

                if image.content_type not in allowed_types:
                  logger.warning(f"Invalid image uploaded: {image.filename}")

                  raise HTTPException(
                status_code=400,
                detail="Only PNG and JPG images are allowed."
            )
                        # STEP 8 - Read image
                content = await image.read()
                print("Content length:", len(content))

                if len(content) == 0:
                 logger.warning(f"Empty image uploaded: {image.filename}")

                raise HTTPException(
                  status_code=400,
                  detail="Uploaded image is empty."
            )
            # STEP 9 - Reset file pointer
                await image.seek(0)
                        # STEP 10 - Save image
                safe_filename = os.path.basename(image.filename)

                file_path = os.path.join(
                  UPLOAD_DIR,
                  safe_filename
        )

                with open(file_path, "wb") as buffer:
                  shutil.copyfileobj(image.file, buffer)

                logger.info(f"Image stored at {file_path}")
                        # STEP 11 - Generate answer
                answer = await generate_answer(question)
                        # STEP 12 - Return response
                return {
                  "message": "Final API executed successfully",
                  "question": question,
                  "image": image.filename,
                  "answer": answer,
                  "status": "Final API working"
        }
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Final API failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
