from sqlalchemy import Column, Integer, String, DateTime, Enum, func
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from app.enums import Gender

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(11), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=True) 
    gender = Column(Enum(Gender), nullable=False) 
    location = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)
    
    farmer = relationship("Farmer", back_populates="user", uselist=False)  
    buyer = relationship("Buyer", back_populates="user", uselist=False) 
    # products = relationship("Product", back_populates="user") 
    
    
