"""Ask a question across one or more uploaded papers; prints the answer with citations.

Run: python -m app.rag.ask "Compare U-Net and nnU-Net for liver segmentation" unet nnunet
     python -m app.rag.ask "What dataset did the U-Net paper use?"   # no keys = whole corpus
"""

import json
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-opus-5-5"
CACHE_PATH = Path(__file__).resolve().parents[2] / ".cache" / "file_ids.json"


def ask(question: str, paper_keys: list[str] | None = None) -> None:
    papers = json.loads(CACHE_PATH.read_text())
    keys = paper_keys or list(papers.keys())

    content = [{"type": "text", "text": question}]
    for key in keys:
        paper = papers[key]
        content.append({
            "type": "document",
            "source": {"type": "file", "file_id": paper["file_id"]},
            "title": paper["title"],
            "citations": {"enabled": True},
        })

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": content}],
    )

    for block in response.content:
        if block.type != "text":
            continue
        print(block.text)
        for citation in block.citations or []:
            pages = f"p.{citation.start_page_number}-{citation.end_page_number}"
            print(f"  [{citation.document_title}, {pages}] \"{citation.cited_text[:100]}\"")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.rag.ask QUESTION [paper_key ...]")
        sys.exit(1)
    ask(sys.argv[1], sys.argv[2:] or None)
