from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_SHEET_ID: str
    YT_PLAYLIST_URL: str
    DATE_AFTER: str = "20040101"
    START_ROW: int = 1
    LIST_ID: int = 0

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


settings = Settings()