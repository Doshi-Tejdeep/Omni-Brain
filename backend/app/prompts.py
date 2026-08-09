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
You are a helpful AI assistant answering questions about a document.

Use the context below to answer the question. Summarize, infer, and
synthesize from the context as needed — you do not need an exact
matching sentence to answer.

Only say you cannot find the answer if the context is completely
unrelated to the question.

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
