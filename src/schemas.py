from pydantic import BaseModel, Field

class CategoryResponse(BaseModel):
    category_id: int
    name: str = Field(max_length=100)
    description: str | None = None

class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str | None = None