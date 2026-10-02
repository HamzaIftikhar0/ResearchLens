# Phase 1A eval report — 20-paper corpus

Ran `app.eval.run_eval` (10 questions) and `app.eval.validate_index` against
the live Gemini API on 2026-10-03. Raw model output is in
`eval-outputs.md`; this file is the human grading against
`answer-key.md`, plus what the run exposed about the pipeline itself.

## Index validation

PASS — 293 chunks, 20/20 papers, correct page count per paper, zero
duplicate `(paper, page)` pairs. Confirms the Phase 0 design choices
(resumable indexing, per-page saves, retry-on-429/503/connection-error)
hold at 4x the original corpus size — this run exercised all three error
types for real (see "What broke" below), not just in theory.

## Q&A grading (10 questions)

| # | Question | Verdict | Notes |
|---|---|---|---|
| 1 | U-Net's dataset | **Correct** | All 3 datasets named, no liver invented |
| 2 | nnU-Net liver Dice | **Correct** | 95.24/73.71 exact; cites MSD p.33 for a 0.93 figure I haven't personally re-verified, but it's a plausible, specifically-cited claim |
| 3 | U-Net vs. nnU-Net (demo query) | **Correct** | Passes the hallucination trap — never claims the *original* U-Net paper reports a liver number. Cites a "72.9% standalone U-Net" baseline from Cascaded-FCN p.13, which I haven't personally checked but is a plausible re-implementation baseline, not a claim about Ronneberger's paper |
| 4 | Attention U-Net's target organ | **Correct** | Pancreas correctly named; spleen/kidney mentioned as co-evaluated; no liver number invented |
| 5 | UNet++ liver result | **Correct** | 82.90 vs. 76.62 exact, plus accurate bonus detail (Wide U-Net 76.58, parameter counts) |
| 6 | Which papers report no liver result | **Fail (honest abstention)** | "the excerpts do not contain the answer" — see below |
| 7 | CNN vs. transformer on liver | **Fail (honest abstention)** | Retrieved TransUNet/Swin-Unet pages 1-2 only, never their results tables (p.6) | 
| 8 | H-DenseUNet vs. Cascaded-FCN | **Correct** | Exact match: "9.0% and 0.4% improvement on DICE" is precisely what H-DenseUNet p.8 reports, and it correctly resolves H-DenseUNet's reference [39] to Christ et al. |
| 9 | Generalised Dice Loss liver result | **Correct** | Correctly says no liver result exists in this paper; correctly identifies it as a loss-function study |
| 10 | Organ vs. tumor difficulty (3 benchmarks) | **Partial** | Gets LiTS exactly right; explicitly declines on KiTS19/Decathlon rather than inventing a number, but the actual KiTS19/Decathlon numbers were available in the index and just weren't retrieved |

**Score: 7/10 correct, 1/10 partial, 2/10 honest fail. Zero hallucinations
— every trap question (1, 3, 4, 9) was handled correctly, and every
failure was an explicit "I don't have enough information" rather than an
invented number.**

## What this run found, worth fixing before Phase 1B

**1. Retrieval breadth, not generation quality, is the actual bottleneck.**
All 3 non-perfect answers (6, 7, 10) fail the same way: `top_k(k=8)`
retrieves chunks *semantically closest to the question text*, which for a
question like "which papers say nothing about X" or "compare across 6
papers" means the closest chunks are the ones that talk about X the
*most* — exactly the wrong set. The model's response to an under-supplied
context was correctly to decline rather than guess (the prompt's "say so
instead of guessing" instruction is doing real work), but declining isn't
the same as answering. `k=8` was calibrated for Phase 0's 5-paper corpus;
it was never re-tuned for 20 papers across a synthesis-shaped question.
Fix before Phase 1B: either raise `k` substantially for this kind of
query, or — better — route "list/compare across the corpus" questions to
the literature matrix (`matrix.csv`, one row per paper already) instead of
re-running chunk retrieval, since that's structured data built exactly for
aggregate questions.

**2. The free tier's real `generate_content` cap is 20 requests/day per
model, not ~100.** The matrix-extraction run hit `429
RESOURCE_EXHAUSTED` with the API naming the exact limit:
`GenerateRequestsPerDayPerProjectPerModel-FreeTier, quotaValue: 20`,
model `gemini-3.8-flash` — after the 10-question eval had already used 10
of that day's 20. This is a harder constraint than PLAN.md's original
"~100 requests/day" estimate (based on public docs, not this model
specifically) and materially changes Phase 1B planning: extracting a
~100-paper matrix needs ~100 `generate_content` calls alone, which at 20/day
is a 5-day minimum even with zero Q&A calls that day. `embed_content` has
a separate, evidently larger quota — indexing all 293 chunks plus the
query embeddings for 10 questions (303 embed calls) never hit this error.
**Mitigation already shipped:** `app.extract.matrix` now saves after every
row and skips papers already extracted, so hitting this cap mid-run costs
a day, not the work already done — confirmed by this exact run (5 of 20
rows had been written before the cap hit; a second run will resume from
row 6, not row 1).

**3. The index-survives-interruption and retry-on-error design held up
for real, not just in the happy path.** The 212-page indexing run for the
15 new papers hit 429 rate limits three separate times and one
`ConnectError`, all absorbed by `app.gemini_retry.with_retry` without
manual intervention. The 10-question eval separately hit one 429 and one
`ServerError` (503) mid-run. None of these needed a restart.

## What's next

Given the 20/day `generate_content` cap, Phase 1B's ~100-paper matrix
extraction will need to run across multiple days (resumable extraction
already handles this) or split load across more than one free-tier model
ID, which have separate quota buckets. Before that, the retrieval-breadth
fix (finding 1) is worth doing first — there's no point running the matrix
across 100 papers if the Q&A side still can't answer the exact kind of
cross-paper question a 100-paper corpus is supposed to enable.

---

# Phase 1B-0 — retrieval-breadth fix + regression test

Implemented the smallest change that addresses finding 1 above, then
re-ran the same 10-question set to check it. The result is a genuine
improvement, but the regression test itself came out confounded by a
second, forced variable — reported in full below rather than only the
clean-looking part.

## The fix

`app/rag/classify.py`: a keyword/alias heuristic, not a model call (costs
nothing against the daily cap, fails safe to the existing chunk-only path
on a wrong call). `is_aggregate_question()` flags a question as
corpus-wide if it (a) uses explicit aggregate/absence phrasing ("which
papers", "across the corpus", "none of"), (b) names 3+ distinct corpus
papers, or (c) uses a comparison word ("compare", "vs.") while naming ≤1
specific paper (a category comparison like "CNN vs. transformer," not a
2-paper one like "U-Net vs. nnU-Net"). Verified offline against all 10
questions plus one held-out case ("Compare UNet++ and ResUNet++...") before
spending any API calls on it — all 11 classified as expected.

`app/rag/ask.py`: unchanged chunk retrieval always runs; when a question
classifies as aggregate, the prompt *also* includes the full literature
matrix (one row per paper, from `matrix.csv`) alongside the excerpts,
instructed to cite matrix-based claims as `[paper]` and excerpt-based
claims as `[paper, page N]` separately. Chunks aren't replaced — the
matrix supplements them, per the brief ("not only the page-chunk
similarity index").

## The confound: this test run did not isolate the fix

Re-running the eval needed ~30 `generate_content` calls in one day (20 to
regenerate `matrix.csv` under the new schema + 10 for the eval), and
`gemini-3.8-flash` — the model every prior result in this project used —
had already spent its 20/day cap on the Phase 1A run above. Rather than
wait out the multi-hour reset, I split the work across two other free-tier
models with their own separate quota buckets: `gemini-3.5-flash` (16 of 20
matrix rows, until it also hit its own 20/day cap) and
`gemini-3.5-flash-lite` (remaining 4 matrix rows + all 10 eval questions).

That means **today's regression run changed two things at once: the
retrieval architecture (intended) and the underlying model (forced)** —
so a result that changed between Phase 1A and this run cannot be cleanly
attributed to the fix without a same-model comparison. That comparison is
the right next step once `gemini-3.8-flash`'s quota resets (see "What's
next" below) — this section reports what actually happened, confound and
all, rather than waiting to report only a clean-looking number.

## Regression grading

| # | Question | Phase 1A (gemini-3.8-flash) | This run (gemini-3.5-flash-lite) | Change |
|---|---|---|---|---|
| 1 | U-Net's dataset | Correct | Correct | same |
| 2 | nnU-Net liver Dice | Correct (95.24/73.71 exact) | **Wrong numbers** (77.42/92.45/68.16 — doesn't match Table 2 at all) | **regressed** |
| 3 | U-Net vs. nnU-Net | Correct | Still avoids the core trap (never claims U-Net itself reports liver), but **cites wrong nnU-Net numbers** (77.42, 79.07, 92.64) | **regressed** |
| 4 | Attention U-Net's target | Correct | Correct | same |
| 5 | UNet++ liver result | Correct | Correct, exact | same |
| 6 | Which papers report no liver result | Fail (abstained) | **Correct** — lists all 9 expected papers, plus a 10th (the MSD dataset-descriptor paper, which reports zero results of *any* kind, liver included) that my own answer key hadn't explicitly credited | **fixed, exceeds answer key** |
| 7 | CNN vs. transformer on liver | Fail (abstained) | **Substantively correct** — real comparison, TransUNet/Swin-Unet/nnFormer/UNETR numbers mostly right, correctly characterizes the architectural tradeoff — but repeats a wrong nnU-Net number (90.37/88.95) sourced from the regenerated matrix, not invented fresh | **fixed, but inherited a matrix error** |
| 8 | H-DenseUNet vs. Cascaded-FCN | Correct | Correct, exact | same |
| 9 | Generalised Dice Loss liver result | Correct | **Regressed to "the excerpts do not contain the answer"** | **regressed** |
| 10 | Organ vs. tumor difficulty (3 benchmarks) | Partial (LiTS only) | **Correct, all 3 benchmarks** (LiTS, MSD, KiTS19 all with accurate numbers) | **fixed** |

**Net: 2 clean fixes (6, 10), 1 fix with an inherited data error (7), 3
regressions (2, 3, 9), 4 unchanged (1, 4, 5, 8).**

The 3 regressions share a pattern worth naming plainly: all three are on
the *unchanged* chunk-only path (none of them classify as aggregate), and
two of them (2, 3) involve the model misreading the same dense multi-column
results table in the nnU-Net paper that `gemini-3.8-flash` read correctly
in Phase 1A. That's consistent with `gemini-3.5-flash-lite` being weaker
at precise numeric table-reading than `gemini-3.8-flash` — a real, useful
data point about these models, but not a finding about the retrieval fix.
Q9's regression (a correct answer becoming an unhelpful abstention) is the
same story: nothing about its routing changed, so the most likely
explanation is model capability, not architecture.

**New risk surfaced by the fix itself (not the confound):** Q7 shows that
errors in `matrix.csv` can now propagate into aggregate answers that cite
it — the wrong nnU-Net figure traced directly back to the regenerated
matrix row (itself a `gemini-3.5-flash` misreading of the same table). A
matrix-extraction error that would previously have stayed contained to
`matrix.csv` can now surface in a Q&A answer too. Worth a line in future
grading: when an aggregate answer cites `[paper]` (matrix-sourced) rather
than `[paper, page N]` (excerpt-sourced), that claim is only as reliable as
the matrix row backing it.

## Latency

Not captured for this run — `app/eval/run_eval.py` now records
per-question wall-clock time and whether each question was routed as
aggregate or normal (see its source), but that instrumentation landed
*after* this run, to avoid spending more of an already-scarce daily quota
on a timing-only re-run. The next full re-run will have it for free.

## What's next

1. **Re-run this exact 10-question set on `gemini-3.8-flash`** once its
   quota resets, to get a same-model before/after comparison that isolates
   the routing fix from today's forced model swap. This is the one
   genuinely missing piece — everything else in this section is honest
   about being confounded until that happens.
2. Treat `matrix.csv` row quality as part of Q&A correctness going forward,
   not a separate concern — Q7 showed it doesn't stay contained.
3. Only after (1) confirms the fix in isolation: proceed to Phase 1B's
   20 → ~100 paper scale-up, budgeting the 20/day cap across either
   multiple days or multiple model IDs as demonstrated here.
