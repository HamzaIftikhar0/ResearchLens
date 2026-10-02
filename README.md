# ResearchLens

Upload a batch of research papers, ask questions across all of them, and get
back answers with inline citations plus a structured comparison table
(paper / dataset / model / method / metric / result / limitation).

See [PLAN.md](PLAN.md) for scope, architecture, and phases.

## Status

Early build — Phase 0: proving the core pipeline against a 5-paper
liver-segmentation test corpus, no UI yet.

## Layout

| Folder | What it is |
|---|---|
| `backend/` | FastAPI app and the ingest/RAG/extract pipeline (Python) |
| `frontend/` | React + Vite UI (scaffolded, not wired up yet) |
| `corpus/` | Open-access test papers — U-Net, Attention U-Net, U-Net++, nnU-Net, LiTS |
| `docs/` | Architecture notes, demo script, hand-built answer key |

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
