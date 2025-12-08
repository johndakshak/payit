from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.products import Product
from app.models.farmers import Farmer
from app.models.buyers import Buyer
from app.models.orders import Order
from app.models.product_category import ProductCategoryModel
from app.schema.products_schema import ProductCreate, ProductResponse, ProductUpdate
from ..schema.order_schema import OrderCreate, OrderResponse, OrderUpdate
from app.enums import ProductCategoryEnum, OrderStatusEnum
from app.middleware.auth import User, get_current_user
from app.middleware.auth import authMiddleware


router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def create_order(order_create: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(authMiddleware)):

    # 1️⃣ Get product
    product = db.query(Product).filter(Product.id == order_create.product_id).first()
    if not product:
        raise HTTPException(404, f"Product {order_create.product_id} not found")

    # 2️⃣ Check stock
    if order_create.quantity > product.quantity:
        raise HTTPException(400, f"Only {product.quantity} items left in stock")


    # 4️⃣ Get buyer
    buyer = db.query(Buyer).filter(Buyer.user_id == current_user.id).first()
    if not buyer:
        buyer = Buyer(user_id=current_user.id)
        db.add(buyer)
        db.commit()
        db.refresh(buyer)

    # 5️⃣ Create order
    new_order = Order(
        buyer_id=buyer.id,
        product_id=product.id,
        name=product.name,
        price=product.price,
        quantity=order_create.quantity,
    )
    
    db.add(new_order)

    # 3️⃣ Deduct stock
    product.quantity -= order_create.quantity
    
    db.commit()
    db.refresh(product)
    db.refresh(new_order)

    # 6️⃣ Build response manually
    return {
        "id": new_order.id,
        "buyer_id": new_order.buyer_id,
        "product_id": new_order.product_id,
        "name": new_order.name,
        "price": new_order.price,
        "quantity": new_order.quantity,
        "category": product.category,
        "created_at": new_order.created_at,
        "updated_at": new_order.updated_at
    }