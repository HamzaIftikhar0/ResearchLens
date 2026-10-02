"""Extract corpus/*.pdf page by page, embed each page, save the Phase 0 index.

One embed_content call per page (a list of texts in one call returns a
single combined embedding, not one per page - confirmed by testing). Saves
after every page and skips pages already in the index, so a 429 mid-run
costs a retry, not the whole corpus.

Run: python -m app.ingest.build_index
"""

from pathlib import Path

import pymupdf
from dotenv import load_dotenv
from google import genai

from app.ingest.embeddings import embed_text
from app.ingest.index_store import load_index, save_index

load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parents[2]
CORPUS_DIR = BACKEND_DIR.parent / "corpus"

CORPUS = {
    "unet": {
        "filename": "unet-1505.04597.pdf",
        "title": "U-Net: Convolutional Networks for Biomedical Image Segmentation",
    },
    "attention-unet": {
        "filename": "attention-unet-1804.03999.pdf",
        "title": "Attention U-Net: Learning Where to Look for the Pancreas",
    },
    "unetpp": {
        "filename": "unetpp-1807.10165.pdf",
        "title": "UNet++: A Nested U-Net Architecture for Medical Image Segmentation",
    },
    "nnunet": {
        "filename": "nnunet-1809.10486.pdf",
        "title": "nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation",
    },
    "lits": {
        "filename": "lits-1901.04056.pdf",
        "title": "The Liver Tumor Segmentation Benchmark (LiTS)",
    },
}


def extract_pages(pdf_path: Path) -> list[tuple[int, str]]:
    doc = pymupdf.open(pdf_path)
    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            pages.append((i, text))
    return pages


def main() -> None:
    client = genai.Client()

    try:
        chunks = load_index()
    except FileNotFoundError:
        chunks = []
    done = {(c["paper"], c["page"]) for c in chunks}

    for key, meta in CORPUS.items():
        pages = extract_pages(CORPUS_DIR / meta["filename"])
        new_pages = [p for p in pages if (key, p[0]) not in done]
        if not new_pages:
            print(f"{key}: already indexed ({len(pages)} pages)")
            continue

        for page_num, text in new_pages:
            vector = embed_text(client, text, task_type="RETRIEVAL_DOCUMENT")
            chunks.append({
                "paper": key,
                "title": meta["title"],
                "page": page_num,
                "text": text,
                "vector": vector,
            })
            save_index(chunks)
            print(f"{key}: page {page_num}/{pages[-1][0]} indexed")

    print(f"\n{len(chunks)} chunks in the index")


if __name__ == "__main__":
    main()
