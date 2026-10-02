"""Upload corpus/*.pdf via the Files API once; downstream scripts read .cache/file_ids.json.

Run: python -m app.ingest.upload_corpus
"""

import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parents[2]
CORPUS_DIR = BACKEND_DIR.parent / "corpus"
CACHE_PATH = BACKEND_DIR / ".cache" / "file_ids.json"

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


def main() -> None:
    client = anthropic.Anthropic()
    result = {}

    for key, meta in CORPUS.items():
        pdf_path = CORPUS_DIR / meta["filename"]
        uploaded = client.files.upload(file=pdf_path)
        result[key] = {
            "file_id": uploaded.id,
            "filename": meta["filename"],
            "title": meta["title"],
        }
        print(f"{key}: {uploaded.id} ({meta['filename']})")

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(result, indent=2))
    print(f"\nWrote {len(result)} file_ids to {CACHE_PATH}")


if __name__ == "__main__":
    main()
