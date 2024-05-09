from database import Base
from sqlalchemy import Column, String, Integer


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    photo = Column(String)
    address = Column(String)
    hashed_password = Column(String)
