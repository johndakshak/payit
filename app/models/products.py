from sqlalchemy import Column, Integer, String, DateTime, Enum, func, DECIMAL, ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(Enum('grains', 'tubers', 'vegetables', 'fruits', 'livestock', 'cereals', 'oils', 'latex'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    user = relationship("User", back_populates="products")
    