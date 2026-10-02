"""Ask a question across the indexed corpus; prints a cited answer.

Aggregate/corpus-wide questions (see app.rag.classify) also get the
literature matrix as context, not just page chunks - a chunk-similarity
search surfaces evidence for a specific claim well and surfaces "which
papers don't mention X" badly, since the closest chunks to an absence
question are the ones that most discuss the thing being asked about.

Run: python -m app.rag.ask "Compare U-Net and nnU-Net for liver segmentation"
"""

import os
import sys

from dotenv import load_dotenv
from google import genai

from app.extract.matrix import load_existing_rows
from app.gemini_retry import with_retry
from app.ingest.embeddings import embed_text
from app.ingest.index_store import load_index, top_k
from app.rag.classify import is_aggregate_question

load_dotenv()

# Overridable so a day's work can be split across the free tier's separate
# per-model quotas (e.g. CHAT_MODEL=gemini-3.5-flash) without editing code.
CHAT_MODEL = os.environ.get("CHAT_MODEL", "gemini-3.8-flash")

PROMPT_TEMPLATE = """Answer the question using only the labelled excerpts below.
Cite every claim as [paper, page N], using the labels exactly as given - do
not invent a page number that isn't attached to an excerpt you used. If the
excerpts don't contain the answer, say so instead of guessing.

{excerpts}

Question: {question}"""

AGGREGATE_PROMPT_TEMPLATE = """This question needs evidence from across the
whole corpus, not just a few chunks - so you have two sources: labelled
excerpts (specific page-level evidence) and a one-row-per-paper summary
table (built from every paper in the corpus). Use the summary table to make
sure you consider every paper, and the excerpts for supporting detail and
citations. Cite excerpt-based claims as [paper, page N]; cite matrix-based
claims as [paper] (summary table). If neither source answers the question,
say so instead of guessing.

Paper summaries (one row per paper in the corpus):
{matrix}

Labelled excerpts:
{excerpts}

Question: {question}"""


def format_matrix_summaries(rows: list[dict]) -> str:
    return "\n\n".join(
        f"[{r['paper']}]\n"
        f"Dataset: {r['dataset']}\n"
        f"Model: {r['model']}\n"
        f"Method: {r['method']}\n"
        f"Metric: {r['metric']}\n"
        f"Result: {r['result']}\n"
        f"Limitation: {r['limitation']}"
        for r in rows
    )


def ask(question: str, k: int = 8) -> tuple[str, list[dict]]:
    client = genai.Client()
    chunks = load_index()

    query_vector = embed_text(client, question, task_type="RETRIEVAL_QUERY")
    retrieved = top_k(query_vector, chunks, k=k)
    excerpts = "\n\n".join(
        f"[{c['title']}, page {c['page']}]\n{c['text']}" for c in retrieved
    )

    if is_aggregate_question(question):
        matrix = format_matrix_summaries(load_existing_rows())
        prompt = AGGREGATE_PROMPT_TEMPLATE.format(
            matrix=matrix, excerpts=excerpts, question=question
        )
    else:
        prompt = PROMPT_TEMPLATE.format(excerpts=excerpts, question=question)

    response = with_retry(lambda: client.models.generate_content(
        model=CHAT_MODEL,
        contents=[prompt],
    ))

    return response.text, retrieved


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.rag.ask QUESTION")
        sys.exit(1)
    answer, retrieved = ask(sys.argv[1])
    print(answer)
    print("\nRetrieved from:")
    for c in retrieved:
        print(f"  [{c['title']}, page {c['page']}]")
