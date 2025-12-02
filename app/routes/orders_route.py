from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.products import Product
from app.models.farmers import Farmer
from app.models.orders import Order
from app.models.product_category import ProductCategoryModel
from app.schema.products_schema import ProductCreate, ProductResponse, ProductUpdate
from ..schema.order_schema import OrderCreate, OrderResponse, OrderUpdate
from app.enums import ProductCategoryEnum, OrderStatusEnum
from app.middleware.auth import User, get_current_user
from app.middleware.auth import authMiddleware


router = APIRouter(prefix="/orders", tags=["Orders"])


    # id: int
    # buyer_id: int
    # product_id: int
    # name: str
    # price: float
    # quantity: int
    # category: str
    # created_at: datetime
    # updated_at: datetime

    # class OrderCreate(BaseModel):
    # name: 
    # product_id:
    # quantity:


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_order(order_create: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(authMiddleware)):

    product_name = db.query(Product).filter(Product.name == order_create.name).all()
    if not product_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product name: {order_create.name} not found!"
        )
    
    product_id = db.query(Product).filter(Product.id == order_create.product_id).all()
    if not product_id:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product id: {order_create.product_id} not found!"
        )
    
    return {
         "message": "id found!"
    }
