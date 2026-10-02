# ResearchLens

Upload a batch of research papers, ask questions across all of them, and get
back answers with inline citations plus a structured comparison table
(paper / dataset / model / method / metric / result / limitation).

See [PLAN.md](PLAN.md) for scope, architecture, and phases.

## Status

Phase 1B-0: a 20-paper liver-segmentation test corpus, indexed and
evaluated against a 10-question hand-built answer key; a retrieval-breadth
fix implemented and tested, with an honest regression table rather than a
clean-looking one — the test run was confounded by a forced model swap
(daily quota), so the fix works but hasn't yet been isolated from that
confound. No UI yet. See [docs/eval-report.md](docs/eval-report.md).

## Layout

| Folder | What it is |
|---|---|
| `backend/` | FastAPI app and the ingest/RAG/extract/eval pipeline (Python) |
| `frontend/` | React + Vite UI (scaffolded, not wired up yet) |
| `corpus/` | 20 open-access test papers — see `corpus/README.md` |
| `docs/` | Architecture notes, hand-built answer key, eval report |

## Engineering findings

Two things this project caught by actually running against the live API,
not by reading documentation:

- **`embed_content` called with a list of texts returns one combined
  embedding for the whole list, not one embedding per item** — this
  contradicted what public docs and search results said, and the first
  indexing run silently produced 5 chunks instead of 81 before the count
  was checked. Index-cardinality validation (`app.eval.validate_index`)
  exists specifically to catch this class of bug before it reaches
  evaluation; indexing was changed to one page per embedding call.
- **The free tier's real daily cap for `generate_content` is 20 requests
  per model, not the ~100/day general docs suggested** — discovered when
  matrix extraction hit `429 RESOURCE_EXHAUSTED` mid-run, naming the exact
  quota. Both the indexing and extraction scripts save incrementally and
  skip already-done work, so hitting a cap mid-run costs the remainder of
  that day, not progress already made.
- **Free-tier quota buckets are per-model, not shared** — confirmed by
  hitting `gemini-3.8-flash`'s cap mid-task and finding `gemini-3.5-flash`
  and `gemini-3.5-flash-lite` both had fresh quota. Useful for spreading a
  day's work across models, but not free: a weaker substitute model
  misread the same results table `gemini-3.8-flash` had read correctly,
  and that error then propagated from the matrix export into a Q&A answer
  that cited it — matrix quality is now part of Q&A correctness, not a
  separate concern.

Full write-up, including a retrieval-breadth limitation the 10-question
eval exposed and the fix for it: [docs/eval-report.md](docs/eval-report.md).

## Run it

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set GEMINI_API_KEY (free, no card: aistudio.google.com/app/apikey)

python -m app.ingest.build_index
python -m app.rag.ask "Compare U-Net and nnU-Net for liver segmentation"
python -m app.extract.matrix
```

Runs entirely on Gemini's free tier — see [PLAN.md](PLAN.md) section 9.

## Keep secrets out of git

`backend/.env` holds your API key and git ignores it. Never commit it or paste it anywhere.
