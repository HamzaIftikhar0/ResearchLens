"""Run the 10-question eval set against the indexed corpus; writes raw
output (plus per-question latency and aggregate-routing classification) to
docs/eval-outputs.md for manual grading against docs/answer-key.md.

This script runs the questions and records what the pipeline said -
grading that output against the answer key is a separate, human step
(see docs/eval-report.md). Keeping the two apart means re-running the
questions never silently overwrites a prior grading.

Run: python -m app.eval.run_eval
"""

import time
from datetime import datetime, timezone
from pathlib import Path

from app.rag.ask import CHAT_MODEL, ask
from app.rag.classify import is_aggregate_question

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


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [f"# Eval run output (ungraded)\n\nModel: `{CHAT_MODEL}` · Run: {timestamp}\n"]
    latencies = {"normal": [], "aggregate": []}

    for i, question in enumerate(QUESTIONS, start=1):
        aggregate = is_aggregate_question(question)
        print(f"[{i}/{len(QUESTIONS)}] {'[aggregate] ' if aggregate else ''}{question}")

        start = time.monotonic()
        answer, retrieved = ask(question)
        elapsed = time.monotonic() - start
        latencies["aggregate" if aggregate else "normal"].append(elapsed)

        lines.append(f"## Q{i}. {question}")
        lines.append(f"*routed: {'aggregate (matrix + excerpts)' if aggregate else 'normal (excerpts only)'} · {elapsed:.1f}s*\n")
        lines.append(f"{answer}\n")
        lines.append("**Retrieved from:**")
        for c in retrieved:
            lines.append(f"- [{c['title']}, page {c['page']}]")
        lines.append("")

    for label, values in latencies.items():
        if values:
            print(f"{label}: {len(values)} questions, avg {sum(values)/len(values):.1f}s, max {max(values):.1f}s")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines))
    print(f"\nWrote {len(QUESTIONS)} answers to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
