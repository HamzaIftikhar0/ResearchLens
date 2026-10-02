"""Extract one literature-matrix row per indexed paper; writes docs/matrix.csv.

Grade the output against docs/answer-key.md by hand before trusting it on a
bigger corpus - that's the whole point of Phase 0/1A. Saves after every row
and skips papers already in the CSV, so hitting the free tier's daily
generate_content cap mid-run costs only the papers not yet done, not the
rows already extracted.

Run: python -m app.extract.matrix
"""

import csv
import os
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

from app.gemini_retry import with_retry
from app.ingest.index_store import load_index

load_dotenv()

# Overridable so a day's work can be split across the free tier's separate
# per-model quotas (e.g. CHAT_MODEL=gemini-3.5-flash) without editing code.
MODEL = os.environ.get("CHAT_MODEL", "gemini-3.8-flash")
OUTPUT_PATH = Path(__file__).resolve().parents[3] / "docs" / "matrix.csv"

EXTRACTION_PROMPT = """Read the attached paper excerpts (each marked with its
page number) and extract, for the literature matrix:
- dataset: what data it was evaluated on (name, size, modality)
- model: the architecture/model name
- method: the core technique in one sentence
- metric: what metric(s) results are reported in
- result: the key reported number(s), with enough context to be meaningful
  on their own
- limitation: a real limitation the paper itself states or that follows
  directly from its results

If the paper is not primarily about liver segmentation, say so plainly in
`dataset` or `limitation` rather than inventing a liver-specific number that
is not in the text.

Paper excerpts:
{excerpts}"""


class LiteratureMatrixRow(BaseModel):
    dataset: str
    model: str
    method: str
    metric: str
    result: str
    limitation: str


FIELDNAMES = ["key", "paper", "dataset", "model", "method", "metric", "result", "limitation"]


def papers_from_index(chunks: list[dict]) -> dict[str, dict]:
    papers = defaultdict(lambda: {"title": None, "pages": []})
    for c in chunks:
        papers[c["paper"]]["title"] = c["title"]
        papers[c["paper"]]["pages"].append((c["page"], c["text"]))
    return papers


def extract_one(client: genai.Client, pages: list[tuple[int, str]]) -> LiteratureMatrixRow:
    excerpts = "\n\n".join(f"[page {page}]\n{text}" for page, text in sorted(pages))
    response = with_retry(lambda: client.models.generate_content(
        model=MODEL,
        contents=[EXTRACTION_PROMPT.format(excerpts=excerpts)],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=LiteratureMatrixRow,
        ),
    ))
    return response.parsed


def load_existing_rows() -> list[dict]:
    if not OUTPUT_PATH.exists():
        return []
    with OUTPUT_PATH.open(newline="") as f:
        return list(csv.DictReader(f))


def save_rows(rows: list[dict]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    client = genai.Client()
    papers = papers_from_index(load_index())

    rows = load_existing_rows()
    done = {r["key"] for r in rows}

    for key, paper in papers.items():
        if key in done:
            print(f"{key}: already extracted")
            continue
        row = extract_one(client, paper["pages"])
        rows.append({"key": key, "paper": paper["title"], **row.model_dump()})
        save_rows(rows)
        print(f"{key}: {row.dataset} | {row.model} | {row.result}")

    print(f"\n{len(rows)}/{len(papers)} rows in {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
