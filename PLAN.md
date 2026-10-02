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
    task_type=RETRIEVAL_DOCUMENT) — batched one call per paper, not per
    page, to stay well inside the free tier's daily request budget
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

### Phase 1 — Whole corpus, matrix complete
Run indexing and extraction across the full test corpus (up to ~100 papers,
batched to respect the free-tier request budget).
Done when: the full matrix matches the hand-built answer key, and 10 example
questions (including cross-paper ones like the U-Net vs. nnU-Net comparison)
grade out correct.

### Phase 2 — API + real vector DB
Wrap Phase 0/1 in FastAPI; swap the brute-force JSON/numpy index for Chroma.
Done when: the same 10 example questions still answer correctly through the
Chroma-backed retrieval path.

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

**$0.** Every call in Phase 0–1 runs on Gemini's free tier. The only ongoing
constraint is the free tier's daily request cap (reported around 100
requests/day) — see Risks for how the pipeline stays well under it.

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
- **Free-tier rate limit** (~100 requests/day) could block a long debugging
  session → batch embedding calls per paper, not per page (Phase 0's whole
  run is ~20 requests); if the cap is ever hit, wait for the daily reset —
  never add a card to get around it.
- **Copyright on redistributing papers in a public demo** → keep the corpus
  private/gitignored, or restrict any public demo to open-access papers
  only; a video demo avoids the question entirely.
- **Scope creep into "generic chat with PDF"** → rule in section 1; matrix
  correctness is graded before any chat-UI polish happens.

## 11. First 5 tasks
1. ~~Pull 10 open-access liver-segmentation papers into `corpus/`, hand-write
   the answer key~~ — done: `corpus/`, `docs/answer-key.md`.
2. ~~Scaffold `backend/` (FastAPI) and `frontend/` (Vite) skeletons~~ — done.
3. Script: build the index — extract, chunk, embed (batched per paper),
   save `{text, paper, page, vector}` to a local JSON file.
4. Script: embed a question, brute-force retrieve top-k chunks, ask Gemini
   for a cited answer; grade against the answer key.
5. Script: one structured-extraction call per paper; grade the matrix
   against the answer key.
