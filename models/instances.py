from pydantic import BaseModel
class CreateUser(BaseModel):
    user_name: str
    email: str
    password: str
    first_name :str
    last_name :str
    photo :str
    address :str
    cart_id : int
    role :int
    favorites : str

class CreateProduct(BaseModel):
    title: str
    name: str
    photo: str
    price: float
    description: str
    amount: int
    category: str
    tags: str