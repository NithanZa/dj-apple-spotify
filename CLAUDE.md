# Rekordbox Migrator

Spec: `docs/outline.md`. Read it before starting work.

## Priorities

- Phase 1 (feasibility proof) comes first. Do not build batch automation, matching, or UI pages until a single hot cue has been transferred to a Spotify entry and survives a rekordbox restart.
- Safety over coverage: skip uncertain tracks rather than writing questionable data.

## Hard rules

- Never write to the live rekordbox database (`master.db`) while rekordbox is running. Work on copies; back up before any write.
- Never commit rekordbox databases, analysis files, backups, or `.env`.
- Never fabricate Spotify entries by editing Apple Music rows. Spotify entries must be created by rekordbox itself.
- Backend binds to `127.0.0.1` only.

## Tooling

- Backend: `uv` (Python 3.12). Run from `backend/`: `uv run pytest`, `uv run ruff check .`, `uv run ruff format .`.
- Frontend: `pnpm` (not npm). Run from `frontend/`: `pnpm dev`, `pnpm build`, `pnpm lint`.
- Dev ports: frontend 3000, backend 8000. Vite proxies `/api` to the backend.
