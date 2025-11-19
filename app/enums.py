from fastapi import FastAPI
from pydantic import BaseModel, Field
from enum import Enum

class Gender(str, Enum):
    M = "M"
    F = "F"

class Category(str, Enum):
    BUYER = "buyer"
    FARMER = "farmer"





