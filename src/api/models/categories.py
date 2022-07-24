from .base import BaseOrmModel


class Category(BaseOrmModel):
    id: int
    name: str
    emoji: str | None
