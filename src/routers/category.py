from fastapi.routing import APIRouter
from typing import List
from ..db import get_db
from ..schemas import CategoryResponse, CategoryCreate
from ..moduls import Categories



router = APIRouter()


@router.get('/', response_model=List[CategoryResponse])
def get_all_categories():
    with get_db() as session:
        return session.query(Categories).all()

@router.post('/')
def create_category(
    data: CategoryCreate
):
    print(data)