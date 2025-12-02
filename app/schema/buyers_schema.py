from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.enums import Gender, Category  

class Buyers(BaseModel):
    id: int
    user_id: int

    model_config = {"from_attributes": True}