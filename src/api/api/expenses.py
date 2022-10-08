import datetime as dt

from fastapi import (
    APIRouter,
    Depends,
    Query,
    HTTPException,
    status,
    Path,
)

from .. import tables
from ..models.expenses import (
    Expense,
    AggregatedExpense,
    Summary,
)
from ..services.expenses import ExpensesService
from ..services.users import get_user

router = APIRouter()


def get_dates_range_params(date_from: dt.date = Query(...),
                           date_to: dt.date = Query(...)) -> dict:
    if date_from > date_to:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "date_to must be bigger than date_from")

    return {"date_from": date_from, "date_to": date_to}


def split(value: str | None):
    return [v.strip().lower() for v in value.split(",")] if value is not None else None


# TODO: сделать по нормальному
def get_sorting_params(sort_by: str | None = Query(None, description="Comma separated fields", example="date,amount"),
                       asc: str | None = Query(None, description="Comma separated bool values", example="false,true")):
    if sort_by is None and asc is not None:
        asc = None

    bools = {
        '0': False,
        'off': False,
        'f': False,
        'false': False,
        'n': False,
        'no': False,
        '1': True,
        'on': True,
        't': True,
        'true': True,
        'y': True,
        'yes': True,
    }

    split_sort_by = split(sort_by)
    split_asc = split(asc)

    if split_sort_by is not None and not all(split_sort_by):
        raise HTTPException(422, "fields must not be empty")

    if split_sort_by is not None and asc is not None:
        if not (len(split_sort_by) == len(split_asc)):
            raise HTTPException(422, "lengths must be the same")

    if asc is not None:
        try:
            split_asc = [bools[value] for value in split_asc]
        except KeyError:
            raise HTTPException(422, "asc must be bool")

    return {"sort_by": split_sort_by, "asc": split_asc}


# TODO: добавить авторизацию
@router.get("/users/{user_id}/expenses", response_model=list[Expense])
async def get_expenses(user: tables.User = Depends(get_user),
                       service: ExpensesService = Depends(ExpensesService),
                       dates_range=Depends(get_dates_range_params),
                       is_expense: bool | None = Query(None),
                       category: str | None = Query(None),
                       limit: int | None = Query(None, gt=0),
                       sort_by: str = Query("date"),
                       asc: bool | None = Query(True)):
    return service.get_list(user.id,
                            is_expense=is_expense,
                            limit=limit,
                            sort_by=sort_by,
                            asc=asc,
                            category=category,
                            **dates_range)


@router.get("/users/{user_id}/expenses/aggregated/{aggregation_name}", response_model=AggregatedExpense)
async def get_aggregated_expenses(user: tables.User = Depends(get_user),
                                  service: ExpensesService = Depends(ExpensesService),
                                  aggregation_name: str = Path(..., example="date,category"),
                                  agg_func: str = Query(...),
                                  dates_range: dict = Depends(get_dates_range_params),
                                  sorting_param: dict = Depends(get_sorting_params),
                                  is_expense: bool = Query(None)):
    return service.get_aggregated(user.id,
                                  group_by=aggregation_name.split(","),
                                  agg_func=agg_func,
                                  is_expense=is_expense,
                                  **dates_range,
                                  **sorting_param)


@router.get("/users/{user_id}/summary", response_model=Summary)
async def get_summary(dates_range: dict = Depends(get_dates_range_params),
                      service: ExpensesService = Depends(ExpensesService)):
    return service.get_summary(**dates_range)
