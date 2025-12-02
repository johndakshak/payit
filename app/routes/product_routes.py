from fastapi import APIRouter, HTTPException, status, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.products import Product
from app.models.farmers import Farmer
from app.models.product_category import ProductCategoryModel
from app.schema.products_schema import ProductCreate, ProductResponse, ProductUpdate
from app.enums import ProductCategoryEnum
from app.middleware.auth import User, get_current_user
from app.middleware.auth import authMiddleware
import os
import aiofiles
from uuid import UUID, uuid4


router = APIRouter(prefix="/products", tags=["Products"])

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

    
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(current_user: User = Depends(authMiddleware), db: Session = Depends(get_db),

    name: str = Form(...),
    description: str = Form(...),
    img_url: UploadFile = File(...),
    price: str = Form(...),
    quantity: str = Form(...),
    category: str = Form(...),
    location: str = Form(...),
):
    # 1️⃣ Convert category string → Enum
    try:
        category_enum = ProductCategoryEnum(category)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid category. Ensure it matches the allowed Enum values."
        )

    # 2️⃣ Ensure the product category exists
    category_row = db.query(ProductCategoryModel).filter(ProductCategoryModel.name == category_enum).first()

    if not category_row:
        category_row = ProductCategoryModel(name=category_enum)
        db.add(category_row)
        db.commit()
        db.refresh(category_row)
        

    # 3️⃣ Ensure current user has a Farmer profile
    farmer = db.query(Farmer).filter(Farmer.user_id == current_user.id).first()
    if not farmer:
        farmer = Farmer(user_id=current_user.id)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)

    # 4️⃣ Handle image upload
    MAX_FILE_SIZE = 5 * 1024 * 1024 
    allowed_extens = ["jpeg", "png", "jpg"]
    file_exten = img_url.filename.split(".")[-1].lower()

    if file_exten not in allowed_extens:
        raise HTTPException(status_code=400, detail="Invalid file extension!")

    filename = f"{uuid4()}.{file_exten}"
    file_path = f"{UPLOAD_DIR}/{filename}"

    try:
        # Read file content
        content = await img_url.read()

        # Check size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must not be more than 5MB"
            )

        # Save file
        async with aiofiles.open(file_path, "wb") as out_file:
            await out_file.write(content)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An internal server error occured: {e}"
            )

    # 5️⃣ Create the product
    new_product = Product(
        name=name,
        description=description,
        img_url=file_path,
        price=float(price),
        quantity=int(quantity),
        category=category_enum.value,  
        location=location,
        farmer_id=farmer.id,           
        category_id=category_row.id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get('/', status_code=status.HTTP_302_FOUND)
def get_all_products(current_user: User = Depends(authMiddleware), db: Session = Depends(get_db)):
    farmers_products = db.query(Product).all()
    return farmers_products

@router.get('/{farmer_id}', status_code=status.HTTP_302_FOUND)
def get_products_by_farmer(farmer_id: int, db: Session = Depends(get_db), current_user: User = Depends(authMiddleware)):
    product = db.query(Product).filter(Product.farmer_id == farmer_id).all()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No product found for farmer Id: {farmer_id}"
        )
    return product

@router.put('/{product_id}', status_code=status.HTTP_200_OK)
def update_products(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(authMiddleware)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product Id: {product_id} not found for User: {current_user.name}",
                    
        )
    
    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete('/{product_id}', status_code=status.HTTP_200_OK)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(authMiddleware)):

    product = db.query(Product).filter(Product.id == product_id).first()    

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product Id: {product_id} not found for User: {current_user.name}",
                    
        )
    
    db.delete(product)
    db.commit()
    return {
        "success": True,
        "message": f"Product Id: {product_id} deleted successfully!"
    }

