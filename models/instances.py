from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name :str
    last_name :str
    photo :str
    address :str
    role: int

class CreateProduct(BaseModel):
    title: str
    photo: str
    price: float
    description: str
    amount: int
    category: str
    tags: str


class UpdateProduct(BaseModel):
    title: Optional[str] = None
    photo: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    amount: Optional[int] = None
    category: Optional[str] = None
    tags: Optional[str] = None


class CreateOrder(BaseModel):
    user_id: int
    done: bool
    created_at:datetime
    products:str
    