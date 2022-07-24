from fastapi import (
    HTTPException,
    status,
    Depends,
)
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session


def get_user(user_id: int, session: Session = Depends(get_session)) -> tables.User:
    user = session.query(tables.User).filter(tables.User.id == user_id).first()

    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user
