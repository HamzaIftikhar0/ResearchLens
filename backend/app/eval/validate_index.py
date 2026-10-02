"""Validate the chunk index against the corpus: right page counts per paper,
no duplicate (paper, page) chunks, no paper missing entirely.

Run: python -m app.eval.validate_index
"""

from app.ingest.build_index import CORPUS, CORPUS_DIR, extract_pages
from app.ingest.index_store import load_index


def main() -> None:
    chunks = load_index()
    ok = True

    seen = set()
    for c in chunks:
        key = (c["paper"], c["page"])
        if key in seen:
            print(f"DUPLICATE: {key}")
            ok = False
        seen.add(key)

    for key, meta in CORPUS.items():
        expected = len(extract_pages(CORPUS_DIR / meta["filename"]))
        actual = sum(1 for c in chunks if c["paper"] == key)
        status = "ok" if expected == actual else "MISMATCH"
        if status != "ok":
            ok = False
        print(f"{key}: expected {expected} pages, indexed {actual} [{status}]")

    missing = set(CORPUS) - {c["paper"] for c in chunks}
    if missing:
        print(f"MISSING PAPERS (never indexed): {missing}")
        ok = False

    verdict = "PASS" if ok else "FAIL"
    print(f"\n{verdict}: {len(chunks)} chunks, {len(CORPUS)} papers in the manifest")


if __name__ == "__main__":
    main()
