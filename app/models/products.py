from sqlalchemy import Column, Integer, String, DateTime, Enum, func, DECIMAL, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from enums import ProductCategoryEnum

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    img_url = Column(String(255), nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(Enum(ProductCategoryEnum), nullable=False) 
    location = Column(String(255), nullable=False)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("product_category.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    
    # category_obj = relationship("ProductCategory", back_populates="products")
    farmer = relationship("Farmer", back_populates="products")
    orders = relationship("Order", back_populates="product") 
    # user = relationship("User", back_pop
    

    