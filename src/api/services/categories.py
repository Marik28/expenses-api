from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import get_session
from ..tables import Category


class CategoriesService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self) -> list[Category]:
        return self.session.query(Category).order_by(Category.name).all()
