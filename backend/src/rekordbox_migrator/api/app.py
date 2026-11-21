from fastapi import FastAPI

from rekordbox_migrator import __name__ as pkg_name

app = FastAPI(title="Rekordbox Migrator")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": pkg_name}
