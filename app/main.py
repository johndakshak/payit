import logging
from fastapi import FastAPI
from models.base import Base
from models.user import User
from models.product_category import ProductCategoryModel  
from models.products import Product 
from models.farmers import Farmer
from models.buyers import Buyer
from models.orders import Order
from database import engine
from routes import users_routes
from routes import product_routes
from routes import auth_route
from routes import product_category_routes
from routes import orders_route
from routes import cloudinary_routes
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routes import oauth_routes
from routes import cloudinary_routes
import os
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "PayIt App",
    version = "0.0.1",
    description = "Our Market Place For Farmers And Buyers"
    )

# app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(users_routes.router)
app.include_router(product_routes.router)
app.include_router(auth_route.router)
app.include_router(product_category_routes.router)
app.include_router(orders_route.router)
app.include_router(oauth_routes.router)
app.include_router(cloudinary_routes.router)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv,
    https_only=False,
)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #allow specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
@app.get('/')
def home():
    return {
        "status": "success",
        "message": "Hello world"
    }