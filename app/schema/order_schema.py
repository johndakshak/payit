from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class OrderCreate(BaseModel):
    name: str = Field(..., max_length=50)
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be a positive integer")
    

    @field_validator('name')
    def no_whitespace(cls, v):
        v = v.strip()  
        if not v:
            raise ValueError('must not be empty or whitespace')
        return v

    model_config = {"from_attributes": True}


class OrderUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    buyer_id: int
    product_id: int
    name: str
    price: float
    quantity: int
    category: str
    created_at: datetime
    updated_at: datetime


