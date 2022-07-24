import datetime as dt
from decimal import Decimal

from .base import BaseOrmModel
from .categories import Category


class Expense(BaseOrmModel):
    id: int
    date: dt.date
    is_expense: bool
    amount: Decimal
    comment: str | None
    category: Category


class AggregatedExpense(BaseOrmModel):
    amount: list[Decimal]
    date: list[dt.date] | None
    category: list[str] | None
