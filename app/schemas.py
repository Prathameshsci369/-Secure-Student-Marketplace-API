from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str

    model_config = {"from_attributes": True}

class ProductBase(BaseModel):
    title: str
    description: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    seller_id: int
    file_path: str
    is_approved: bool

    model_config = {"from_attributes": True}




