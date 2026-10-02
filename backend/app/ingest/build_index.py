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
    "3dunet": {
        "filename": "3dunet-1606.06650.pdf",
        "title": "3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation",
    },
    "vnet": {
        "filename": "vnet-1606.04797.pdf",
        "title": "V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation",
    },
    "hdenseunet": {
        "filename": "hdenseunet-1709.07330.pdf",
        "title": "H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes",
    },
    "cascadedfcn-liver": {
        "filename": "cascadedfcn-liver-1702.05970.pdf",
        "title": "Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks",
    },
    "msd": {
        "filename": "msd-2106.05735.pdf",
        "title": "The Medical Segmentation Decathlon",
    },
    "msd-dataset": {
        "filename": "msd-dataset-1902.09063.pdf",
        "title": "A large annotated medical image dataset for the development and evaluation of segmentation algorithms",
    },
    "transunet": {
        "filename": "transunet-2102.04306.pdf",
        "title": "TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation",
    },
    "swinunet": {
        "filename": "swinunet-2105.05537.pdf",
        "title": "Swin-Unet: Unet-like Pure Transformer for Medical Image Segmentation",
    },
    "nnformer": {
        "filename": "nnformer-2109.03201.pdf",
        "title": "nnFormer: Interleaved Transformer for Volumetric Segmentation",
    },
    "unetr": {
        "filename": "unetr-2103.10504.pdf",
        "title": "UNETR: Transformers for 3D Medical Image Segmentation",
    },
    "resunetpp": {
        "filename": "resunetpp-1911.07067.pdf",
        "title": "ResUNet++: An Advanced Architecture for Medical Image Segmentation",
    },
    "doubleunet": {
        "filename": "doubleunet-2006.04868.pdf",
        "title": "DoubleU-Net: A Deep Convolutional Neural Network for Medical Image Segmentation",
    },
    "segresnet": {
        "filename": "segresnet-1810.11654.pdf",
        "title": "3D MRI brain tumor segmentation using autoencoder regularization",
    },
    "gdl": {
        "filename": "gdl-1707.03237.pdf",
        "title": "Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations",
    },
    "kits19": {
        "filename": "kits19-1912.01054.pdf",
        "title": "The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge",
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
