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

## 4. Pipeline — v1 (no vector DB yet)

```
PDF upload
  → Files API (upload once, keep the file_id)
  → per question: send the relevant paper(s) as `document` blocks,
    citations enabled
  → Claude answers, cites paper + page
  → separate call, per paper: structured extraction
    (output_config.format, JSON schema) → one matrix row
  → UI: chat view + matrix table view, CSV export
```

A fact that changes the architecture: Claude's context window is 1M tokens
and PDF documents support native page-level citations
(`citations: {enabled: true}` on a `document` content block) — but that's
incompatible with structured JSON output on the *same* call. So
Q&A-with-citations and matrix-extraction are always two separate calls,
never one. For a library under roughly 30–40 papers, whole relevant PDFs can
go straight into context instead of hand-rolling retrieval — simpler, and
the citations are exact page numbers, not a chunk-overlap guess.

## 5. Pipeline — v2 (the scaling layer: embeddings + vector DB)

Once a library is bigger than comfortably fits in context, or re-sending
full PDFs per question gets expensive, add retrieval in front of the same
two calls:

```
PDF → text + layout extraction (PyMuPDF)
  → section-aware chunking (Abstract/Methods/Results/Limitations)
  → embeddings (third-party — Claude has no first-party embeddings
    endpoint; Voyage AI or a local sentence-transformers/BGE model)
  → vector store (Chroma to start; pgvector-on-Postgres is the
    production swap, reusing the HEMS backend stack)
  → top-k retrieval → same citation-enabled document/text call
```

This is the layer that actually earns the "RAG + embeddings + vector DB"
line on the CV — v1 proves the product works, v2 proves you understand why
retrieval exists and when it's needed instead of defaulting to it on day one.

## 6. Tech stack

| Layer | Choice | Why |
|---|---|---|
| LLM | Claude API — `claude-opus-5-5` by default; `claude-sonnet-5-5` as the budget tier for everyday Q&A once cost matters (your call to make when you wire it up, not a silent downgrade) | Native PDF citations, 1M context, structured outputs |
| Structured extraction | `output_config.format` + `client.messages.parse()` | current API — the schema-validated path, not the deprecated `output_format` param |
| PDF handling | Files API (`client.files.upload`) | upload once, reference by `file_id` across every question |
| Embeddings (v2) | Voyage AI, or a local sentence-transformers/BGE model for zero API cost | Anthropic has no native embeddings endpoint |
| Vector DB (v2) | Chroma (embedded, zero infra) → pgvector on Postgres later | Chroma for speed now; pgvector reuses what HEMS already taught you |
| Backend | FastAPI | same stack as the HEMS backend, no new framework to learn |
| Frontend | React + Vite, minimal | upload, chat, table — not a design project |
| Storage | Local filesystem for PDFs (S3-compatible later); SQLite/Postgres for metadata and matrix rows | |

## 7. Folder layout

```
ResearchLens/
  PLAN.md
  backend/
    app/
      ingest/        PDF upload, Files API bookkeeping
      rag/            question -> citation-enabled answer
      extract/        structured literature-matrix extraction
      retrieval/      v2: chunking, embeddings, vector store
      api/            FastAPI routes
  frontend/          React + Vite app
  corpus/            open-access liver-segmentation test papers (gitignored if license is unclear)
  docs/              architecture notes, demo script, hand-built answer key for grading
```

## 8. Phases and milestones

### Phase 0 — Prove the core call (days, not weeks; no UI)
Script: upload 5–10 corpus papers via the Files API, ask "what dataset did
paper X use", get a cited answer; separately, extract the matrix row for
each of those papers.
Done when: 5 manually-checked questions return correct, correctly-cited
answers, and the matrix is right for those 5 papers.

### Phase 1 — Whole corpus, matrix complete
Run both calls across the full test corpus (up to ~100 papers, batched).
Done when: the full matrix matches a hand-built answer key you write
yourself, and 10 example questions (including cross-paper ones like the
U-Net vs. nnU-Net comparison) grade out correct.

### Phase 2 — API + v2 retrieval layer
Wrap Phase 0/1 in FastAPI; add chunking + embeddings + Chroma; add a
size/cost threshold that switches a library from "whole PDFs in context" to
"retrieve top-k chunks first."
Done when: a library past the threshold still answers the same 10 example
questions correctly through the retrieval path.

### Phase 3 — Frontend
Upload flow, chat UI with visible citations (paper + page), matrix table
view, CSV export.
Done when: upload → ask → compare → export runs end to end without touching
the API docs.

### Phase 4 — Polish for the CV
Demo video (the U-Net vs. nnU-Net query is the money shot), README with an
architecture diagram, a short write-up of the v1-vs-v2 retrieval decision —
it's a genuine design call, so say so. Host a small public demo only with
open-access papers, or ship a recorded demo instead if hosting real papers
is a copyright risk.

## 9. Numbers to hit (quality, not revenue)

| Metric | Floor | Good |
|---|---|---|
| Citation correctly points at the supporting page | 85% | 98% |
| Matrix field accuracy vs. hand-built answer key | 70% | 90% |
| Cross-paper comparison questions graded correct | 70% | 90% |
| End-to-end answer latency | < 15s | < 5s |
| Library size handled before switching to v2 retrieval | 30 papers | 100+ papers |

## 10. Costs (monthly, while building/demoing)

| Item | USD |
|---|---|
| Claude API (dev + demo volume, mixed Opus/Sonnet) | 5–20 |
| Embeddings (v2, if hosted rather than local) | 0–5 |
| Hosting (only if a public demo ships; a recorded demo instead = $0) | 0–10 |
| **Total** | **~5–35** |

## 11. Risks and what we do about them

- **Hallucinated citations** (answer cites a page that doesn't support the
  claim) → every answer must use Claude's native `citations` feature, not a
  free-text "according to paper X" — then spot-check cited pages by hand
  during Phase 0/1 grading, not just trust the feature.
- **PDF layout chaos** (two-column papers, tables, figures) breaks naive
  text extraction in v2 → v1's whole-PDF approach sidesteps this almost
  entirely, which is another reason it comes first.
- **Copyright on redistributing papers in a public demo** → keep the corpus
  private/gitignored, or restrict any public demo to open-access papers
  only; a video demo avoids the question entirely.
- **Scope creep into "generic chat with PDF"** → rule in section 1; matrix
  correctness is graded before any chat-UI polish happens.
- **Structured output and citations can't run in one call** → already
  designed around in section 4; don't try to merge them later to "save a
  call."

## 12. First 5 tasks if this plan is approved
1. Pull 10 open-access liver-segmentation papers (arXiv/PMC) into `corpus/`,
   and hand-write the answer key (matrix rows + 5 Q&A pairs) before writing
   any code.
2. Scaffold `backend/` (FastAPI) and `frontend/` (Vite) skeletons; no logic
   yet.
3. Script: Files API upload for the 10 papers, store the `file_id`s.
4. Script: one citation-enabled Q&A call against the corpus; grade against
   the answer key.
5. Script: one structured-extraction call per paper; grade the matrix
   against the answer key.
