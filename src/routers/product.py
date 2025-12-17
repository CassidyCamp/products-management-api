from typing import Annotated, List
from fastapi.routing import APIRouter
from fastapi import Depends, Body, HTTPException, status, Query, Path
from ..schemas import ProductResponse, ProductCreate
from ..db import get_db
from sqlalchemy.orm import Session
from ..moduls import Products, Categories

router = APIRouter(tags=['Products'])

@router.get('/', response_model=List[ProductResponse])
def get_all_product(session: Annotated[Session, Depends(get_db)]):
    # return {}
    return session.query(Products).all()


@router.post('/', response_model=ProductResponse)
def create_product(product_data: Annotated[ProductCreate, Body], session: Annotated[Session, Depends(get_db)]):
    
    if not session.query(Categories).get(product_data.category_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found.')
        
    new_product = Products(name=product_data.name, price=product_data.price, category_id=product_data.category_id, in_stock=product_data.in_stock)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product


@router.get('/search', response_model=List[ProductResponse])
def search_product_by_name(name: Annotated[str, Query(min_length=2)], session: Annotated[Session, Depends(get_db)]):
    product = session.query(Products).filter(Products.name.ilike(f'%{name}%')).all()
    return product


@router.get('/filter/category', response_model=List[ProductResponse])
def search_product_by_name(category: Annotated[str, Query(min_length=2)], session: Annotated[Session, Depends(get_db)]):
    getCategory = session.query(Categories).filter(Categories.name.ilike(f'%{category}%')).first()
    
    if not getCategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
    
    return getCategory.products


@router.get('/filter/price', response_model=List[ProductResponse])
def search_product_by_name(
    session: Annotated[Session, Depends(get_db)],
    min_price: Annotated[float, Query(ge=0)] = None, 
    max_price: Annotated[float, Query(ge=0)] = None, 
    ):
    
    
        
    product = session.query(Products)
        
    if min_price:
        product = product.filter(Products.price>=min_price)
    if max_price:
        product = product.filter(Products.price<=max_price)
    
    return product.all()
        


@router.get('/{product_id}', response_model=ProductResponse)
def get_product_by_id(product_id: Annotated[int, Path(ge=1)], session: Annotated[Session, Depends(get_db)]):
    product = session.query(Products).get(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
