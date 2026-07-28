from backend.app.prompts import SEARCH_PROMPT


def build_context(chunks):
    """
    Convert retrieved chunks into a single formatted context string.
    """

    context = []

    for chunk in chunks:
        context.append(
            f"[Page {chunk['page_number']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context)


def build_search_prompt(chunks, question):
    """
    Create the final prompt for the LLM.
    """

    context = build_context(chunks)

    prompt = SEARCH_PROMPT.format(
        context=context,
        question=question
    )

    return prompt