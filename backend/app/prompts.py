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
You are a helpful AI assistant.

Answer the user's question using only the retrieved context.

If the answer is not available in the context, say:
"I could not find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
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