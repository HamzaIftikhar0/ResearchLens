"""embed_content wrapper: one text per call - a list of texts in one call
returns a single combined embedding, not one per item (confirmed by
testing, not assumed).
"""

from google import genai
from google.genai import types

from app.gemini_retry import with_retry


def embed_text(client: genai.Client, text: str, task_type: str) -> list[float]:
    response = with_retry(lambda: client.models.embed_content(
        model="gemini-embedding-2",
        contents=[text],
        config=types.EmbedContentConfig(task_type=task_type),
    ))
    return response.embeddings[0].values
