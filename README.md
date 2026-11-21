# Rekordbox Migrator

Local web app that migrates rekordbox 7 tracks from Apple Music to Spotify while keeping hot cues, memory cues, saved loops, and beatgrids. Full spec: [docs/outline.md](docs/outline.md).

**Current status:** scaffold only. Next up is Phase 1 (feasibility proof): move one hot cue from one Apple Music entry to one Spotify entry and confirm it survives a rekordbox restart.

## Layout

```text
backend/    Python 3.12 + FastAPI (uv). Package: src/rekordbox_migrator/
  src/rekordbox_migrator/
    api/         FastAPI app and routes
    rekordbox/   database + analysis-file access (pyrekordbox)
    spotify/     OAuth PKCE, search, playlists
    matching/    Apple Music -> Spotify matching
    migration/   orchestrator, transfer, alignment, validation
    automation/  pywinauto rekordbox UI driving
    backup/      backup + restore
    storage/     migration state (SQLite), snapshots
  tests/
frontend/   React + Vite + TypeScript (pnpm). src/{pages,components,services}
docs/       outline.md (spec)
```

## Run

Backend (http://127.0.0.1:8000):

```sh
cd backend
uv sync
uv run rekordbox-migrator          # set RBM_RELOAD=true for auto-reload
```

Frontend (http://localhost:3000, proxies `/api` to the backend):

```sh
cd frontend
pnpm install
pnpm dev
```

Configuration comes from `RBM_*` environment variables or `backend/.env` (see `backend/.env.example`).

## Checks

```sh
cd backend && uv run pytest && uv run ruff check . && uv run ruff format --check .
cd frontend && pnpm build && pnpm lint
```
