from app.utils.logger import logger

async def generate_answer(question: str) -> str:
    logger.info(f"Generating answer for: {question}")

    return f"Received your question: '{question}'. RAG pipeline is under development."
