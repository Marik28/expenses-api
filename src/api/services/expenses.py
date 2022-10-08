import datetime as dt

import pandas as pd
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_session
from ..settings import settings
from ..tables import (
    Expense,
    Category,
)


class ExpensesService:
    sort_by_mapping = {
        "date": Expense.date,
        "amount": Expense.amount,
        "category": Category.name,
    }

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_list_query(self,
                        user_id: int,
                        date_from: dt.date,
                        date_to: dt.date,
                        is_expense: bool = None,
                        category: str = None,
                        limit: int = None,
                        sort_by: str = "date",
                        asc: bool = True):
        q = (self.session.query(Expense)
             .join(Expense.category)
             .filter(Expense.user_id == user_id)
             .filter(Expense.date.between(date_from, date_to))
             .filter(Expense.category_id.notin_(settings.exclude_categories)))

        if category is not None:
            q = q.filter(Category.name == category)

        if is_expense is not None:
            q = q.filter(Expense.is_expense == is_expense)

        if limit is not None:
            q = q.limit(limit)

        order_by_col = self.sort_by_mapping[sort_by]
        order_by = order_by_col.asc() if asc else order_by_col.desc()
        return q.order_by(order_by)

    def get_list(self, user_id: int, **kwargs) -> list[Expense]:
        query = self._get_list_query(user_id, **kwargs)
        return query.all()

    def get_aggregated(self,
                       user_id: int,
                       group_by: list[str] | None,
                       agg_func: str,
                       sort_by: list[str] | None,
                       asc: list[bool] | None,
                       **kwargs):

        if asc is None:
            asc = True

        query = self._get_list_query(user_id, **kwargs).with_entities(Expense, Category)
        df = pd.read_sql(query.statement, query.session.bind, index_col="id")
        df["amount"] = -df["amount"]
        df.rename(columns={"name": "category"}, inplace=True)
        df = getattr(df[["amount", *group_by]].groupby(group_by), agg_func)().reset_index()

        if sort_by is not None:
            df = df.sort_values(by=sort_by, ascending=asc)

        return df.reset_index().to_dict("list")

    def _get_summary_query(self, expenses: bool, date_from: dt.datetime = None, date_to: dt.datetime = None):
        q = (self.session
             .query(func.sum(Expense.amount).label("sum"))
             .filter(Expense.is_expense.is_(expenses)))
        if date_from and date_to:
            q = q.filter(Expense.date.between(date_from, date_to))

        return q

    def get_summary(self, date_from: dt.datetime = None, date_to: dt.datetime = None):
        revenue = self._get_summary_query(expenses=False, date_from=date_from, date_to=date_to)
        expenses = self._get_summary_query(expenses=True, date_from=date_from, date_to=date_to)
        result = revenue.union(expenses).all()
        return {"revenue": result[1][0], "expenses": result[0][0]}
