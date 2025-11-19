from sqlalchemy import Column, Integer, String, DateTime, Enum, func
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from app.enums import Gender, Category

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(50), min_length=3, max_length=30, nullable=False)
    phone = Column(String(11), min_length=11, unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), min_length=6, nullable=True) 
    gender = Column(Enum('M', 'F'), nullable=False) 
    category = Column(Enum('buyer', 'farmer'), nullable=False) 
    location = Column(String(255), min_length=10, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)

    products = relationship("Product", back_populates="user")
