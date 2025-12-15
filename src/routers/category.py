from fastapi.routing import APIRouter
from typing import List
from ..db import get_db
from ..schemas import CategoryResponse, CategoryCreate, CategoryUpdate
from ..moduls import Categories
from fastapi import HTTPException, Path, Depends
from sqlalchemy import text


router = APIRouter(tags=['Categories'])


@router.get('/', response_model=List[CategoryResponse])
def get_all_categories(session = Depends(get_db)):
    return session.query(Categories).all()
    
@router.get('/{category_id}', response_model=CategoryResponse)
def get_one_category(category_id: int = Path(ge=1), session = Depends(get_db)):
    category = session.query(Categories).get(category_id)
    
    if not category:
        raise HTTPException(status_code=404, detail="category not found.")
    
    return category

@router.post('/', response_model=CategoryResponse)
def create_category(data: CategoryCreate, session = Depends(get_db)):
    if session.query(Categories).filter(Categories.name==data.name).first():
        raise HTTPException(status_code=400, detail="category exists")
    
    new_category = Categories(name=data.name, description=data.description)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    
    return new_category

@router.put('/update/{category_id}', response_model=CategoryResponse)
def update_category(
    data: CategoryUpdate,
    category_id: int = Path(ge=1)
):
    with get_db() as session:
        
        category = session.query(Categories).get(category_id)
        
        if not category:
            raise HTTPException(status_code=400, detail="category not found.")
        
        category.name = data.name or category.name
        category.description = data.description or category.description

        session.commit()
        session.refresh(category)
        return category
    
@router.delete('/delete/{category_id}')
def update_category(category_id: int = Path(ge=1)):
    with get_db() as session:
        
        category = session.query(Categories).get(category_id)
        
        if not category:
            raise HTTPException(status_code=400, detail="category not found.")
        
        session.delete(category)
        session.flush()
        
        # if session.query(Categories).count() == 0:
        #     session.execute(text("ALTER SEQUENCE categories_id_seq RESTART WITH 1"))        
        
        session.commit()
        
        return {"message": "category delete"}
    