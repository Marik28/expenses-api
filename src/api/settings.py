from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    port: int = 8001
    db_url: str

    exclude_categories: list[int]


settings = Settings()
