# ResearchLens — AI Literature Review Assistant

Upload a batch of research papers, ask questions across all of them, and get
answers with paper-level citations plus a structured comparison table
(paper / dataset / model / method / metric / result / limitation). Built
around the liver-segmentation internship as the first real use case, not a
generic "chat with your PDF" clone.

---

## 1. The rule that decides everything

**The comparison table ships before the chat gets polished.** A chatbot that
answers questions about PDFs is a weekend project everyone has seen; a tool
that turns 50 papers into a correct, exportable literature matrix is not. If
a feature doesn't move the matrix or the citation accuracy forward, it waits.

**Zero running cost, no exceptions.** Every API this project touches has to
have a real, permanent free tier — not a trial credit that runs out mid-build.
That constraint picked the stack in section 6; it isn't a fallback, it's a
requirement.

**The JSON index is the baseline, not a placeholder to feel bad about.**
Don't add Chroma because "the plan says Phase 2 is Chroma" — add it when
there's a specific, measured reason the brute-force index can't keep up
(section 8's numbers). Keeping the simple version running means a real
before/after comparison is possible later, instead of just asserting a
vector DB helped.

## 2. Scope (v1, and nothing more)

In v1:
- One user, no accounts: a "library" is just a folder of papers.
- Upload 10–100 PDFs into a library.
- Ask free-text questions across a library; answers come back with inline
  citations (paper + page).
- One-click structured extraction into the matrix: Paper | Dataset | Model |
  Method | Metric | Result | Limitation.
- Export the matrix as CSV/Markdown.

Explicitly not in v1: multi-user accounts, billing, real-time collaboration,
non-PDF formats (slides, Word), automatic paper discovery (arXiv crawling),
fine-tuning anything, mobile app.

## 3. Test corpus

The liver-segmentation papers from the internship: U-Net, Attention U-Net,
U-Net++, nnU-Net, and the LiTS/liver-dataset papers. This is both the dogfood
set and the demo script — "Compare U-Net and nnU-Net for liver segmentation"
is the actual first query to get working, not a placeholder example. Use
open-access versions (arXiv / PMC) so the corpus can also appear in a public
demo without copyright problems — see Risks.

## 4. Pipeline

```
PDF (local, corpus/)
  → text extraction per page (PyMuPDF — `import pymupdf`, the `fitz` alias
    is deprecated) — gives exact page numbers for free
  → one chunk per page (simple; good enough at this corpus size)
  → embed every chunk (Gemini `embed_content`, model `gemini-embedding-2`,
    task_type=RETRIEVAL_DOCUMENT) — one call per page: a list of texts in
    one `embed_content` call returns a single combined embedding, not one
    per item, confirmed by testing (see the eval report, not assumed from
    docs)
  → store {text, paper, page, vector}:
      Phase 0 — a JSON file + brute-force cosine similarity in numpy
                (fast enough for a few hundred chunks, no infra needed)
      Phase 2 — swap the storage/search step for Chroma; nothing else
                in the pipeline changes
  → question: embed it (task_type=RETRIEVAL_QUERY), retrieve top-k chunks,
    build a prompt where each chunk is labelled [paper, page N], ask
    Gemini (`gemini-3.8-flash`) to answer using only those labelled
    chunks and to cite them
  → structured extraction: feed a paper's chunk text back to Gemini with
    `response_schema=LiteratureMatrixRow`, `response_mime_type=
    "application/json"` → read `response.parsed`, one call per paper
```

Why this looks different from a typical "upload PDF, ask Claude" design:
Gemini has no native page-grounded citation primitive the way Claude's
`citations: {enabled: true}` is — verified directly against the docs, not
assumed. So the shortcut an Anthropic-based v1 could use (hand the model a
whole PDF, trust its built-in citations, skip chunking) isn't available
here. Chunking and embeddings move from "a scaling optimization for later"
to "required from day one," because labelling each chunk with its real page
number *during indexing* is the only way citations are grounded in fact
rather than the model guessing a page number from memory. That's not a
downgrade — it's the real RAG pipeline the original pitch wanted, just
arriving in Phase 0 instead of Phase 2.

## 5. Tech stack

| Layer | Choice | Why |
|---|---|---|
| LLM | Gemini API — `gemini-3.8-flash` | genuinely free tier, native structured JSON output |
| Embeddings | Gemini API — `gemini-embedding-2` | free tier, native embeddings endpoint |
| PDF extraction | PyMuPDF | local, free, gives exact page numbers |
| Retrieval (Phase 0) | Brute-force cosine similarity over a JSON index, in numpy | a few hundred vectors doesn't justify a real vector DB yet |
| Retrieval (Phase 2) | Chroma (embedded) → pgvector on Postgres later | swap in once the corpus outgrows brute-force search |
| Backend | FastAPI | same stack as the HEMS backend, no new framework to learn |
| Frontend | React + Vite, minimal | upload, chat, table — not a design project |
| Storage | Local filesystem for PDFs (S3-compatible later); SQLite/Postgres for metadata and matrix rows | |

## 6. Folder layout

```
ResearchLens/
  PLAN.md
  backend/
    app/
      ingest/        PDF -> text -> chunks -> embeddings -> index
      rag/            question -> retrieval -> cited answer
      extract/        structured literature-matrix extraction
      api/            FastAPI routes (from Phase 2)
  frontend/          React + Vite app
  corpus/            open-access liver-segmentation test papers (gitignored if license is unclear)
  docs/              architecture notes, demo script, hand-built answer key for grading
```

## 7. Phases and milestones

### Phase 0 — Prove the core pipeline (days, not weeks; no UI)
Build the index for 5–10 corpus papers (extract, chunk, embed, store as
JSON + numpy); ask the 5 answer-key questions through retrieval; extract the
matrix row for each of those papers.
Done when: 5 manually-checked questions return correct, correctly-cited
answers, and the matrix is right for those 5 papers.

### Phase 1A — 20-paper corpus: validate at a small step up, not a big one
Expand 5 → 20 papers; re-run indexing (confirms resume/retry still hold,
not just the design); validate index integrity (page counts, no
duplicates, no missing papers — `app.eval.validate_index`); expand the
Q&A set to 10 questions including ones that only make sense at this size
(cross-paper comparisons, "which papers say nothing about X"); run it, and
write down the actual graded accuracy — `docs/eval-report.md`, not just a
feeling that it worked.
Done when: index validation passes, and the 10-question report exists with
real pass/fail per question, not just a vibe.
**Status: done — see `docs/eval-report.md`. 7/10 correct, 1 partial, 2 honest
abstentions (no hallucinations), plus two real findings (retrieval breadth
fails on cross-paper aggregate questions; the free tier's real
`generate_content` cap is 20/day per model, not ~100) that change Phase 1B.**

### Phase 1B-0 — Retrieval-breadth fix + regression test
Smallest possible change, nothing else: classify a question as
corpus-wide/aggregate (`app.rag.classify`, keyword/alias heuristic, no
model call) and, only for those, add the full literature matrix to the
prompt alongside the unchanged chunk excerpts — not instead of them.
Re-run the same 10-question set and compare per-question against Phase 1A.
No Chroma, no embeddings changes, no section-aware chunking, no fancier
classifier — PLAN.md section 1's rule about not adding infrastructure
before measuring the need applies here too.
Done when: the regression table shows the previously-failing aggregate
questions fixed, the previously-passing ones still pass, and the
comparison was run on the *same model* as Phase 1A so the fix is isolated
from unrelated variables.
**Status: done.** Phase 1A complete, retrieval-breadth fix implemented,
matrix independently verified against source (19/20 rows correct, the 1
error hand-corrected to 20/20). First regression attempt was confounded by
`gemini-3.8-flash`'s quota forcing a substitute-model test
(`gemini-3.5-flash`/`-lite`) — 2 clean fixes, 1 fix with an inherited data
error, 3 regressions, all traced to the substitute model being weaker at
precise table-reading, not to the fix. **Clean same-model regression on
`gemini-3.8-flash` the next day: 10/10 correct, zero hallucinations, zero
regressions from Phase 1A** — confirms the hypothesis exactly (Q2/Q3/Q9
recovered to correct; Q6/Q7/Q10 fixed with no inherited errors now that
the matrix is correct too). Full table in `docs/eval-report.md`. Phase 1B
is unblocked.

### Phase 1B — ~100 papers
Build the full ~100-paper corpus
and re-run the same evaluation (index validation + the 10-question set,
extended if needed) at that scale. Extraction alone will take multiple
days at a 20/day generate_content cap unless load is spread across more
than one free-tier model id — already demonstrated as a working pattern in
1B-0, so budget for it rather than being surprised by it again. Also carry
forward 1B-0's finding that matrix-row errors can surface in Q&A answers
now, not just in the matrix export — grade matrix quality as part of Q&A
correctness, not separately.
Done when: the full matrix matches the hand-built answer key, and the
10-question set (plus any cross-paper questions specific to the larger
corpus) grades out correct.

### Phase 2 — API + real vector DB
Wrap Phase 0/1 in FastAPI; swap the brute-force JSON/numpy index for Chroma
— only once section 8's numbers say brute-force search is actually the
bottleneck, per the rule in section 1. Measure before/after on the same
10-question set so the vector DB's benefit is demonstrated, not asserted.
Done when: the same question set still answers correctly through the
Chroma-backed retrieval path, with a measured latency/accuracy comparison
against the JSON-index baseline.

### Phase 3 — Frontend
Upload flow, chat UI with visible citations (paper + page), matrix table
view, CSV export.
Done when: upload → ask → compare → export runs end to end without touching
the API docs.

### Phase 4 — Polish for the CV
Demo video (the U-Net vs. nnU-Net query is the money shot), README with an
architecture diagram, a short write-up of *why* retrieval was built from day
one instead of deferred — it's a real design call forced by the zero-cost
constraint, and explaining it is more interesting than hiding it. Host a
small public demo only with open-access papers, or ship a recorded demo
instead if hosting real papers is a copyright risk.

## 8. Numbers to hit (quality, not revenue)

| Metric | Floor | Good |
|---|---|---|
| Citation correctly points at the supporting page | 85% | 98% |
| Matrix field accuracy vs. hand-built answer key | 70% | 90% |
| Cross-paper comparison questions graded correct | 70% | 90% |
| End-to-end answer latency | < 15s | < 5s |
| Chunks handled by brute-force search before needing Chroma | 500 | 2,000+ |

## 9. Costs

**$0.** Every call runs on Gemini's free tier. The ongoing constraint is
the free tier's daily cap — measured directly from a real `429` error, not
estimated from docs: `generate_content` on `gemini-3.8-flash` is capped at
**20 requests/day**; `embed_content` has a separate, evidently larger quota
(293 embedding calls plus 10 query embeddings in one day never hit it).
See Risks for how the pipeline stays resilient to this.

## 10. Risks and what we do about them

- **Hallucinated citations** (answer cites a page that doesn't support the
  claim) → the model only ever sees page-labelled chunks, never the raw
  question alone, so a citation can only reference a page we actually
  retrieved — then spot-check cited pages by hand during Phase 0/1 grading,
  since "the label exists" isn't the same as "the label is the right page
  for that specific claim."
- **PDF layout chaos** (two-column papers, tables, figures) can scramble
  per-page text extraction → accept some noise in Phase 0 (per-page chunks
  are coarse enough to tolerate most of it); only invest in smarter,
  column-aware extraction if answer-key grading actually fails because of it.
- **Free-tier daily cap** (20 `generate_content` requests/day per model,
  confirmed by hitting it) could block a long session → both indexing and
  extraction save incrementally and skip already-done work, so the cap
  costs a day's wait, not lost progress (confirmed: a run that hit the cap
  mid-extraction resumed cleanly from where it stopped). If the cap is hit,
  wait for the daily reset or switch to a different free-tier model id for
  the rest of that day's work — never add a card to get around it.
- **Retrieval breadth fails on cross-paper aggregate questions**
  ("which papers don't mention X", "compare across the whole corpus") →
  `top_k` similarity search surfaces chunks closest to the question, which
  for an absence/aggregate question is exactly the wrong set. Found during
  Phase 1A grading (`docs/eval-report.md`), not before. The model declined
  rather than hallucinating when under-supplied, which is the correct
  fallback behavior — but it's still a wrong answer. Fix before Phase 1B:
  route this question shape at the literature matrix instead of chunk
  retrieval.
- **Copyright on redistributing papers in a public demo** → keep the corpus
  private/gitignored, or restrict any public demo to open-access papers
  only; a video demo avoids the question entirely.
- **Scope creep into "generic chat with PDF"** → rule in section 1; matrix
  correctness is graded before any chat-UI polish happens.

## 11. First 5 tasks — all done (Phase 0 + 1A)
1. ~~Pull papers into `corpus/`, hand-write the answer key~~ — done: 20
   papers, `docs/answer-key.md` (10 Q&A pairs + a 20-row matrix).
2. ~~Scaffold `backend/` (FastAPI) and `frontend/` (Vite) skeletons~~ — done.
3. ~~Script: build the index~~ — done: `app.ingest.build_index`, one
   `embed_content` call per page, resumable, retries 429/503/connection
   errors. 293 chunks, validated by `app.eval.validate_index`.
4. ~~Script: retrieve + ask, grade against the answer key~~ — done:
   `app.rag.ask` + `app.eval.run_eval`; graded in `docs/eval-report.md`.
5. ~~Script: structured extraction per paper, grade the matrix~~ — done:
   `app.extract.matrix` (resumable; hit and survived the real 20/day cap
   mid-run).

Next tasks are Phase 1B's, listed in section 7.
