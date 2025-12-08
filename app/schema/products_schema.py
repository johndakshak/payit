from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.enums import ProductCategoryEnum

class ProductCreate(BaseModel):
    name: str = Field(..., max_length=50)
    description: str
    img_url: str
    location: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    category: ProductCategoryEnum

    @field_validator('name')
    def no_whitespace(cls, v):
        v = v.strip()  
        if not v:
            raise ValueError('must not be empty or whitespace')
        return v

    model_config = {"from_attributes": True}

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    img_url: str
    price: float
    quantity: int
    category: ProductCategoryEnum
    location: str
    farmer_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    img_url: Optional[str] = None
    location: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, gt=0)
    category: Optional[ProductCategoryEnum] = None

    @field_validator('name')
    def no_whitespace(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError('must not be empty or whitespace')
        return v

    model_config = {"from_attributes": True}
