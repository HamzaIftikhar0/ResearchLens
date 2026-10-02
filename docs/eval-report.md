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
