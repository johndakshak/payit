from sqlalchemy import Column, Integer, String, DateTime, Enum, func, DECIMAL, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Buyer(Base):
    __tablename__ = 'buyers'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)  

    user = relationship("User", back_populates="buyer")
    orders = relationship("Order", back_populates="buyer")
    
    