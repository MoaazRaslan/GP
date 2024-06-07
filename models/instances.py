from pydantic import BaseModel,EmailStr
from typing import Optional


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name :str
    last_name :str
    photo :str
    address :str

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
