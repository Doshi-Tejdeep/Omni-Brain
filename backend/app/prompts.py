from langchain_core.prompts import PromptTemplate

RAG_PROMPT = PromptTemplate.from_template(
"""
You are an AI assistant.

Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

If the answer cannot be found, reply:
"I could not find the answer in the provided documents."
"""
)

SEARCH_PROMPT = PromptTemplate.from_template(
"""
Use the retrieved context to answer accurately.

Context:
{context}

Question:
{question}
"""
)

SQL_PROMPT = PromptTemplate.from_template(
"""
Generate an SQL query if database information is required.

Question:
{question}
"""
)

VISION_PROMPT = PromptTemplate.from_template(
"""
Analyze the provided image or chart.

Question:
{question}
"""
)
