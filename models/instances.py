from pydantic import BaseModel
class CreateUser(BaseModel):
    user_name: str
    email: str
    password: str
    first_name :str
    last_name :str
    photo :str
    address :str
    cart_id : str
    role :int
    favorites : str
