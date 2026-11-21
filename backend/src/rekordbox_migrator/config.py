from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RBM_", env_file=".env", extra="ignore")

    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = False
    data_dir: Path = Path.home() / ".rekordbox-migrator"
    spotify_client_id: str = ""
    spotify_redirect_uri: str = "http://127.0.0.1:8000/api/spotify/callback"


settings = Settings()
