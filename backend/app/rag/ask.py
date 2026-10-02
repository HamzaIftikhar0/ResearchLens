"""Ask a question across the indexed corpus; prints a cited answer.

Run: python -m app.rag.ask "Compare U-Net and nnU-Net for liver segmentation"
"""

import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.ingest.build_index import EMBED_MODEL
from app.ingest.index_store import load_index, top_k

load_dotenv()

CHAT_MODEL = "gemini-3.8-flash"

PROMPT_TEMPLATE = """Answer the question using only the labelled excerpts below.
Cite every claim as [paper, page N], using the labels exactly as given - do
not invent a page number that isn't attached to an excerpt you used. If the
excerpts don't contain the answer, say so instead of guessing.

{excerpts}

Question: {question}"""


def ask(question: str, k: int = 8) -> None:
    client = genai.Client()
    chunks = load_index()

    query_vector = client.models.embed_content(
        model=EMBED_MODEL,
        contents=[question],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    ).embeddings[0].values

    retrieved = top_k(query_vector, chunks, k=k)
    excerpts = "\n\n".join(
        f"[{c['title']}, page {c['page']}]\n{c['text']}" for c in retrieved
    )

    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=[PROMPT_TEMPLATE.format(excerpts=excerpts, question=question)],
    )

    print(response.text)
    print("\nRetrieved from:")
    for c in retrieved:
        print(f"  [{c['title']}, page {c['page']}]")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.rag.ask QUESTION")
        sys.exit(1)
    ask(sys.argv[1])
