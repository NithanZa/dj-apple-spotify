def main() -> None:
    import uvicorn

    from rekordbox_migrator.config import settings

    uvicorn.run(
        "rekordbox_migrator.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
