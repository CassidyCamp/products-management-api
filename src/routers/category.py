from fastapi.routing import APIRouter
from typing import List, Annotated
from ..db import get_db
from ..schemas import CategoryResponse, CategoryCreate, CategoryUpdate
from ..moduls import Categories
from fastapi import HTTPException, Path, Depends, status
from sqlalchemy.orm import Session


router = APIRouter(tags=['Categories'])


@router.get('/', response_model=List[CategoryResponse])
def get_all_categories(session: Annotated[Session, Depends(get_db)]):
    return session.query(Categories).all()

    
@router.get('/{category_id}', response_model=CategoryResponse)
def get_one_category(category_id: Annotated[int, Path(ge=1)], session: Annotated[Session, Depends(get_db)]):
    category = session.query(Categories).get(category_id)
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found.")
    
    return category


@router.post('/', response_model=CategoryResponse)
def create_category(data: CategoryCreate, session: Annotated[Session, Depends(get_db)]):
    
    if session.query(Categories).filter(Categories.name==data.name).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this name already exists")
    
    new_category = Categories(name=data.name, description=data.description)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    
    return new_category


@router.put('/update/{category_id}', response_model=CategoryResponse)
def update_category(data: CategoryUpdate, category_id: Annotated[int, Path(ge=1)], session: Annotated[Session, Depends(get_db)]):
    category = session.query(Categories).get(category_id)
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
    
    if session.query(Categories).filter(Categories.name==data.name).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with name 'Electronics' already exists")
    
    category.name = data.name or category.name
    category.description = data.description or category.description

    session.commit()
    session.refresh(category)
    return category
    

@router.delete('/delete/{category_id}')
def delete_category(category_id: Annotated[int, Path(ge=1)], session: Annotated[Session, Depends(get_db)]):
    category = session.query(Categories).get(category_id)
    
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="category not found.")
    
    products = category.products.count()
    if products > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot delete category. {products} products are linked to this category")
    
    session.delete(category)
    session.commit()
    return {"message": "Category deleted successfully"}
    
    # if session.query(Categories).count() ==      0:
    #     session.execute(text("ALTER SEQUENCE categories_id_seq RESTART WITH 1"))        
    
    
    