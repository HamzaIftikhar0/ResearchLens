"""Read/write the Phase 0 chunk index: a JSON file of {paper, title, page, text, vector}.

Phase 2 swaps this module out for Chroma; nothing that imports it should
need to change beyond that.
"""

import json
from pathlib import Path

import numpy as np

INDEX_PATH = Path(__file__).resolve().parents[2] / ".cache" / "index.json"


def save_index(chunks: list[dict]) -> None:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(chunks))


def load_index() -> list[dict]:
    return json.loads(INDEX_PATH.read_text())


def top_k(query_vector: list[float], chunks: list[dict], k: int = 8) -> list[dict]:
    query = np.array(query_vector)
    query = query / np.linalg.norm(query)

    vectors = np.array([c["vector"] for c in chunks])
    vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    scores = vectors @ query
    best = np.argsort(-scores)[:k]
    return [chunks[i] for i in best]
