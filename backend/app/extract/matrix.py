"""Extract one literature-matrix row per indexed paper; writes docs/matrix.csv.

Grade the output against docs/answer-key.md by hand before trusting it on a
bigger corpus - that's the whole point of Phase 0.

Run: python -m app.extract.matrix
"""

import csv
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

from app.ingest.index_store import load_index

load_dotenv()

MODEL = "gemini-3.8-flash"
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


def papers_from_index(chunks: list[dict]) -> dict[str, dict]:
    papers = defaultdict(lambda: {"title": None, "pages": []})
    for c in chunks:
        papers[c["paper"]]["title"] = c["title"]
        papers[c["paper"]]["pages"].append((c["page"], c["text"]))
    return papers


def extract_one(client: genai.Client, pages: list[tuple[int, str]]) -> LiteratureMatrixRow:
    excerpts = "\n\n".join(f"[page {page}]\n{text}" for page, text in sorted(pages))
    response = client.models.generate_content(
        model=MODEL,
        contents=[EXTRACTION_PROMPT.format(excerpts=excerpts)],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=LiteratureMatrixRow,
        ),
    )
    return response.parsed


def main() -> None:
    client = genai.Client()
    papers = papers_from_index(load_index())

    rows = []
    for key, paper in papers.items():
        row = extract_one(client, paper["pages"])
        rows.append({"paper": paper["title"], **row.model_dump()})
        print(f"{key}: {row.dataset} | {row.model} | {row.result}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote {len(rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
