"""Does this question need evidence from many/all papers (route to the
literature matrix) or from a narrow set of ~1-2 named papers (route to
page-chunk retrieval)?

top_k chunk retrieval is good at "find the evidence for this specific
claim" and bad at "enumerate or compare across many papers" - the split
follows that line, not the wording of any one test question. Deliberately
a keyword/alias heuristic, not a model call: it costs nothing against the
free tier's daily cap, and a wrong classification fails safe (falls back
to the existing chunk-retrieval path, not a crash).
"""

import re

from app.ingest.build_index import CORPUS

AGGREGATE_PHRASES = [
    "which papers", "what papers", "how many papers",
    "all papers", "every paper", "none of the papers", "no papers",
    "across the corpus", "across this corpus", "in this corpus",
    "whole corpus", "across all",
]

COMPARISON_MARKERS = ["compare", " vs ", "versus", "difference between"]

# One or more recognizable name variants per corpus paper. Matched with
# non-word lookaround (not \b) so "u-net" doesn't spuriously match inside
# "nnu-net", and aliases ending in punctuation (e.g. "unet++") still match -
# a trailing \b fails right after a non-word character like "+".
PAPER_ALIASES = {
    "unet": ["u-net"],
    "attention-unet": ["attention u-net"],
    "unetpp": ["unet\\+\\+", "u-net\\+\\+"],
    "nnunet": ["nnu-net"],
    "lits": ["lits"],
    "3dunet": ["3d u-net"],
    "vnet": ["v-net"],
    "hdenseunet": ["h-denseunet"],
    "cascadedfcn-liver": ["cascaded-fcn", "cascaded fcn"],
    "msd": ["medical segmentation decathlon", "the decathlon", "decathlon"],
    "transunet": ["transunet"],
    "swinunet": ["swin-unet", "swin unet"],
    "nnformer": ["nnformer"],
    "unetr": ["unetr"],
    "resunetpp": ["resunet\\+\\+"],
    "doubleunet": ["doubleu-net", "double u-net"],
    "segresnet": ["segresnet"],
    "gdl": ["generalised dice", "generalized dice"],
    "kits19": ["kits19", "kits-19"],
}


def named_papers(question: str) -> set[str]:
    q = question.lower()
    matched = set()
    for key, aliases in PAPER_ALIASES.items():
        if key not in CORPUS:
            continue
        if any(re.search(rf"(?<!\w){alias}(?!\w)", q) for alias in aliases):
            matched.add(key)
    return matched


def is_aggregate_question(question: str) -> bool:
    q = question.lower()
    if any(phrase in q for phrase in AGGREGATE_PHRASES):
        return True

    matched = named_papers(question)
    if len(matched) >= 3:
        return True
    if len(matched) <= 1 and any(marker in q for marker in COMPARISON_MARKERS):
        return True
    return False
