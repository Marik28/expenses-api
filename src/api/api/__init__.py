from fastapi import APIRouter

from . import expenses

router = APIRouter()
router.include_router(expenses.router)
