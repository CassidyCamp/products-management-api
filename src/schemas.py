from pydantic import BaseModel, Field, ConfigDict
from typing import List




class CategoryResponse(BaseModel):
    category_id: int
    name: str = Field(max_length=100)
    description: str | None = None
    # products: List[ProductResponse] = []
    
    # model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str | None = None

class CategoryUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = None
    
