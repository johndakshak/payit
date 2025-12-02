from sqlalchemy import Column, Integer, String, DateTime, Enum, func, DECIMAL, ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class ProductCategoryModel(Base):
    __tablename__ = 'product_category'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String(100), nullable=False)

    # products = relationship("Product", back_populates="category_obj")