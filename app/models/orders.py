from sqlalchemy import Column, Integer, String, DateTime, Enum, func, DECIMAL, ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    buyer = relationship("Buyer", back_populates="orders")
    product = relationship("Product", back_populates="orders") 
    
       

    
     