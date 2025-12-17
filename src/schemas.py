from pydantic import BaseModel, Field, ConfigDict
from typing import List, Annotated




class CategoryResponse(BaseModel):
    category_id: int
    name: Annotated[str, Field(max_length=100)]
    description: str | None = None
    
    # model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]
    description: Annotated[str | None, Field(max_length=500)] = None

class CategoryUpdate(BaseModel):
    name: Annotated[str | None, Field(min_length=2, max_length=100)] = None
    description: Annotated[str | None, Field(max_length=500)] = None
    

class ProductResponse(BaseModel):
    product_id: int 
    name: Annotated[str, Field(max_length=100)]
    price: float
    in_stock: bool
    category: CategoryResponse
    
    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    category_id: int 
    name: Annotated[str, Field(max_length=100)]
    price: float
    in_stock: bool = True
    