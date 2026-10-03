"""Run the 10-question eval set against the indexed corpus; writes raw
output (plus per-question latency and aggregate-routing classification) to
docs/eval-outputs.md for manual grading against docs/answer-key.md.

Saves after every question (to .cache/eval-outputs.json, then renders
docs/eval-outputs.md from it) and skips questions already answered, same
pattern as app.ingest.build_index and app.extract.matrix - a crash or a
quota cutoff mid-run costs the remaining questions, not the ones already
answered. Starts fresh if CHAT_MODEL differs from the cached run's model,
so a partial run never silently mixes answers from two different models
into one report.

This script runs the questions and records what the pipeline said -
grading that output against the answer key is a separate, human step
(see docs/eval-report.md).

Run: python -m app.eval.run_eval
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from app.rag.ask import CHAT_MODEL, ask
from app.rag.classify import is_aggregate_question

CACHE_PATH = Path(__file__).resolve().parents[2] / ".cache" / "eval-outputs.json"
OUTPUT_PATH = Path(__file__).resolve().parents[3] / "docs" / "eval-outputs.md"

QUESTIONS = [
    "What dataset did the U-Net paper evaluate on?",
    "What liver Dice score did nnU-Net achieve, and on what benchmark?",
    "Compare U-Net and nnU-Net for liver segmentation.",
    "What does Attention U-Net add to U-Net, and what organ does it target?",
    "What liver result did UNet++ report, and against what baseline?",
    "Which papers in this corpus report no liver segmentation result at all?",
    "Compare CNN-based and transformer-based architectures on liver segmentation specifically.",
    "How does H-DenseUNet relate to the Cascaded-FCN-liver paper?",
    "What does the Generalised Dice Loss paper contribute, and does it report a liver result?",
    "Across LiTS, the Decathlon, and KiTS19, how does organ segmentation difficulty compare to tumor segmentation difficulty?",
]


def load_cache() -> dict:
    if not CACHE_PATH.exists():
        return {}
    return json.loads(CACHE_PATH.read_text())


def save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2))


def render_markdown(cache: dict) -> str:
    lines = [f"# Eval run output (ungraded)\n\nModel: `{cache['model']}` · Run: {cache['run_started']}\n"]
    for i, question in enumerate(QUESTIONS, start=1):
        r = cache["results"].get(str(i))
        if r is None:
            continue
        lines.append(f"## Q{i}. {question}")
        routed = "aggregate (matrix + excerpts)" if r["aggregate"] else "normal (excerpts only)"
        lines.append(f"*routed: {routed} · {r['elapsed']:.1f}s*\n")
        lines.append(f"{r['answer']}\n")
        lines.append("**Retrieved from:**")
        for c in r["retrieved"]:
            lines.append(f"- [{c['title']}, page {c['page']}]")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    cache = load_cache()
    if cache.get("model") != CHAT_MODEL:
        if cache:
            print(f"Cached partial run was on {cache.get('model')}, starting fresh for {CHAT_MODEL}")
        cache = {
            "model": CHAT_MODEL,
            "run_started": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "results": {},
        }

    for i, question in enumerate(QUESTIONS, start=1):
        if str(i) in cache["results"]:
            print(f"[{i}/{len(QUESTIONS)}] already answered")
            continue

        aggregate = is_aggregate_question(question)
        print(f"[{i}/{len(QUESTIONS)}] {'[aggregate] ' if aggregate else ''}{question}")

        start = time.monotonic()
        answer, retrieved = ask(question)
        elapsed = time.monotonic() - start

        cache["results"][str(i)] = {
            "answer": answer,
            "retrieved": retrieved,
            "aggregate": aggregate,
            "elapsed": elapsed,
        }
        save_cache(cache)
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(render_markdown(cache))

    done = cache["results"]
    for label in ("normal", "aggregate"):
        values = [r["elapsed"] for r in done.values() if r["aggregate"] == (label == "aggregate")]
        if values:
            print(f"{label}: {len(values)} questions, avg {sum(values)/len(values):.1f}s, max {max(values):.1f}s")

    print(f"\n{len(done)}/{len(QUESTIONS)} answered; see {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
