from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enums import Gender, Category  

class Farmers(BaseModel):
    id: int
    user_id: int

    model_config = {"from_attributes": True}