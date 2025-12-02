from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.middleware.auth import authMiddleware
from app.database import get_db
from app.models.product_category import ProductCategoryModel
from app.schema.product_category_schema import ProductCategoryCreate, ProductCategoryResponse

router = APIRouter(prefix="/categories", tags=["Product Categories"])


@router.get("/", response_model=List[ProductCategoryResponse])
def get_categories(db: Session = Depends(get_db), current_user: User = Depends(authMiddleware)):
    return db.query(ProductCategoryModel).all()

@router.get("/{category_id}", response_model=ProductCategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(authMiddleware)):
    category = db.query(ProductCategoryModel).filter(ProductCategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
