import logging
from fastapi import FastAPI, HTTPException, status
from .models.base import Base
from .models.user import User
from app.database import engine
from .routes import users_routes
from .routes import product_routes
from app.routes import auth_route



logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "PayIt App",
    version = "0.0.1",
    description = "Our Market Place For Framer And Buyers"
    )

app.include_router(users_routes.router)
app.include_router(product_routes.router)
app.include_router(auth_route.router)