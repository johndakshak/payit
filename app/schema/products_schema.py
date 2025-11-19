from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.enums import Gender, Category  


class ProductCreate(BaseModel):
    name: str = Field(..., max_length=50)
    user_id: int
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    quantity: int = Field(..., gt=0, description="Quantity must be a positive integer")
    category: str

    model_config = {"from_attributes": True}


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, gt=0)
    category: Optional[str] = None

    model_config = {"from_attributes": True}


class ProductResponse(BaseModel):
    id: int
    name: str
    user_id: int
    price: float
    quantity: int
    category: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
