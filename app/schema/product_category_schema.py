from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ProductCategoryCreate(BaseModel):
    name: str

    @field_validator('name')
    def no_whitespace(cls, v):
        v = v.strip()  
        if not v:
            raise ValueError('must not be empty or whitespace')
        return v

class ProductCategoryResponse(BaseModel):
    id: int
    name: str


    model_config = {"from_attributes": True}