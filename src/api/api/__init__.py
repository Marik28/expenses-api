from fastapi import APIRouter

from . import expenses
from . import categories

router = APIRouter()
router.include_router(expenses.router)
router.include_router(categories.router)
