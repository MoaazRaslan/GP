from pydantic import BaseModel
class CreateUser(BaseModel):
    username: str
    email: str
    password: str
    first_name :str
    last_name :str
    photo :str
    address :str
    cart_id : int
    role : str
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