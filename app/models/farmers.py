from sqlalchemy import Column, Integer, String, DateTime, Enum, func, DECIMAL, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    user = relationship("User", back_populates="farmer") 
    products = relationship("Product", back_populates="farmer")
    
