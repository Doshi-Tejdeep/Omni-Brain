import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

MODEL_NAME = "gemini-3.5-flash"


def analyze_image(image_path: str, question: str = None) -> str:
    """
    Analyze an image using Google Gemini Vision.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    if not image_bytes:
        raise ValueError(
            "Image file is empty."
        )

    extension = os.path.splitext(image_path)[1].lower()

    if extension == ".png":
        mime_type = "image/png"

    elif extension in {".jpg", ".jpeg"}:
        mime_type = "image/jpeg"

    elif extension == ".webp":
        mime_type = "image/webp"

    else:
        raise ValueError(
            f"Unsupported image format: {extension}"
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = question.strip() if question else ""

    if not prompt:
        prompt = (
            "Analyze this image carefully. "
            "Describe the important information visible "
            "in the image, including text, objects, charts, "
            "tables, diagrams, and other relevant details."
        )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type,
            ),
            prompt,
        ],
    )

    if not response.text:
        return "Gemini returned an empty response."

    return response.text