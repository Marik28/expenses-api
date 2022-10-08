from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    debug: bool = True
    port: int = 8001
    db_url: str

    exclude_categories: list[int]


settings = Settings()
