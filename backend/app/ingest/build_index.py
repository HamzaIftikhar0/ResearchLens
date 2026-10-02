"""Extract corpus/*.pdf page by page, embed each page, save the Phase 0 index.

One embed_content call per paper (batched across that paper's pages) to
stay well inside the free tier's daily request cap.

Run: python -m app.ingest.build_index
"""

from pathlib import Path

import pymupdf
from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.ingest.index_store import save_index

load_dotenv()

EMBED_MODEL = "gemini-embedding-2"
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


def embed_pages(client: genai.Client, texts: list[str]) -> list[list[float]]:
    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )
    return [e.values for e in response.embeddings]


def main() -> None:
    client = genai.Client()
    chunks = []

    for key, meta in CORPUS.items():
        pages = extract_pages(CORPUS_DIR / meta["filename"])
        vectors = embed_pages(client, [text for _, text in pages])

        for (page_num, text), vector in zip(pages, vectors):
            chunks.append({
                "paper": key,
                "title": meta["title"],
                "page": page_num,
                "text": text,
                "vector": vector,
            })
        print(f"{key}: {len(pages)} pages indexed")

    save_index(chunks)
    print(f"\nWrote {len(chunks)} chunks to the index")


if __name__ == "__main__":
    main()
