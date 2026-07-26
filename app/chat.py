from openai import OpenAI

from app.config import CHAT_MODEL, OPENAI_API_KEY

_client = OpenAI(api_key=OPENAI_API_KEY)

_SYSTEM_PROMPT = """You are a helpful tutor for an online course. Answer the
student's question using ONLY the course material provided below. If the
material doesn't contain the answer, say you don't have that information in
the course content — do not use outside knowledge.

Course material:
{context}
"""


def stream_tutor_answer(chunks, question: str):
    if not chunks:
        yield "This course doesn't have any content indexed yet."
        return

    context = "\n\n".join(chunk.content for chunk in chunks)

    stream = _client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        stream=True,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT.format(context=context)},
            {"role": "user", "content": question},
        ],
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta