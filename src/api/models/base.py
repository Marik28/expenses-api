from pydantic import BaseModel


class BaseOrmModel(BaseModel):
    class Config:
        orm_mode = True
