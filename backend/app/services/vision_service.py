import ollama


MODEL_NAME = "gemma3"


def analyze_image(image_path: str, question: str = None) -> str:
    if question:
        prompt = question
    else:
        prompt = (
            "Analyze this image carefully. "
            "Describe what is visible in the image, including important "
            "objects, text, diagrams, screenshots, or other relevant details."
        )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [image_path],
            }
        ],
    )

    return response.message.content