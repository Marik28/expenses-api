from fastapi import APIRouter, Depends

from ..models.categories import Category
from ..services.categories import CategoriesService

router = APIRouter()


@router.get("/categories", response_model=list[Category])
async def get_categories(service: CategoriesService = Depends()):
    return service.get_list()
