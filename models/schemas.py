from database import Base
from sqlalchemy import Column, String, Integer,Double,Date,ForeignKey,ARRAY,Boolean
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    photo = Column(String)
    address = Column(String)
    cart_id = Column(Integer)
    role = Column(Integer)
    favorites = Column(String)
    hashed_password = Column(String)

    user_rate_relation = relationship("Rate",back_populates="rate_user_relation")
    user_order_relation = relationship("Cart",back_populates="order_user_relation")
class Product(Base):
    __tablename__ = "product"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    photo = Column(String)
    price = Column(Double)
    description = Column(String)
    amount = Column(Integer)
    category = Column(String)
    tags = Column(String)
    cnt_voter = Column(Integer, default=0)
    sum_of_stars = Column(Integer, default=0)

    product_rate_relation = relationship("Rate",back_populates="rate_product_relation")
    # product_order_relation = relationship("Cart",back_populates="order_product_relation")
class Rate(Base):
    __tablename__ = "rate"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("user.id"))
    product_id = Column(Integer,ForeignKey("product.id"))
    stars = Column(Integer)

    rate_user_relation = relationship("User",back_populates="user_rate_relation")
    rate_product_relation = relationship("Product",back_populates="product_rate_relation")
class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("user.id"))
    done = Column(Boolean)
    products = Column(String)
    created_at = Column(Date)
    total = Column(Integer)

    order_user_relation = relationship("User",back_populates="user_order_relation")
    # order_product_relation = relationship("Product",back_populates="product_order_relation")

