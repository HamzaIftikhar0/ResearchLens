"""Extract one literature-matrix row per uploaded paper; writes docs/matrix.csv.

Grade the output against docs/answer-key.md by hand before trusting it on a
bigger corpus - that's the whole point of Phase 0.

Run: python -m app.extract.matrix
"""

import csv
import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

MODEL = "claude-opus-5-5"
CACHE_PATH = Path(__file__).resolve().parents[2] / ".cache" / "file_ids.json"
OUTPUT_PATH = Path(__file__).resolve().parents[3] / "docs" / "matrix.csv"

EXTRACTION_PROMPT = """Read the attached paper and extract, for the literature matrix:
- dataset: what data it was evaluated on (name, size, modality)
- model: the architecture/model name
- method: the core technique in one sentence
- metric: what metric(s) results are reported in
- result: the key reported number(s), with enough context to be meaningful on their own
- limitation: a real limitation the paper itself states or that follows directly from its results

If the paper is not primarily about liver segmentation, say so plainly in
`dataset` or `limitation` rather than inventing a liver-specific number that
is not in the text."""


class LiteratureMatrixRow(BaseModel):
    dataset: str
    model: str
    method: str
    metric: str
    result: str
    limitation: str


def extract_one(client: anthropic.Anthropic, file_id: str, title: str) -> LiteratureMatrixRow:
    response = client.messages.parse(
        model=MODEL,
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": EXTRACTION_PROMPT},
                {
                    "type": "document",
                    "source": {"type": "file", "file_id": file_id},
                    "title": title,
                },
            ],
        }],
        output_format=LiteratureMatrixRow,
    )
    return response.parsed_output


def main() -> None:
    papers = json.loads(CACHE_PATH.read_text())
    client = anthropic.Anthropic()

    rows = []
    for key, paper in papers.items():
        row = extract_one(client, paper["file_id"], paper["title"])
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
