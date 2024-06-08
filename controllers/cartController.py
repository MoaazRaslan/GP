from fastapi import APIRouter,HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json
from controllers.authcontroller import get_user_from_token
from models import schemas


def create_cart(db : Session ,token : str):
    user = get_user_from_token(db,token)
    cart = schemas.Cart()
    cart.created_at = datetime.utcnow()
    cart.user_id = user.id
    cart.done = False
    cart.products ="[]"
    cart.total = 0
    db.add(cart)
    db.commit()
    cart = db.query(schemas.Cart).filter(schemas.Cart.done == False ,schemas.Cart.user_id == user.id ).first()
    user.cart_id = cart.id
    db.add(user)
    db.commit()
    return {
        "status":"success",
        "products":cart.products,
        "total":cart.total
    }

async def get_cart(db: Session,token :str):
    user = get_user_from_token(db,token)
    if user.cart_id == 0:
        return create_cart(db,token)
    cart = db.query(schemas.Cart).filter(schemas.Cart.id == user.cart_id).first()
    if cart is None :
        return create_cart(db,token)
    return {
        "status":"success",
        "products":cart.products,
        "total":cart.total
    }

async def end_cart(db : Session, token: str):
    user = get_user_from_token(db,token)
    cart = db.query(schemas.Cart).filter(schemas.Cart.id == user.cart_id).first()
    if cart is None :
        raise HTTPException(status_code=404,detail="Cart not found")
    cart.done = True
    user.cart_id = 0
    db.add(user)
    db.add(cart)
    db.commit()
    return {
        "status":"success"
    }

async def add_element_to_cart(product_id,amount:str,db : Session,token: str):
    amount = int(amount)
    user = get_user_from_token(db,token)
    cart = db.query(schemas.Cart).filter(schemas.Cart.id == user.cart_id).first()
    product = db.query(schemas.Product).filter(schemas.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    if cart is None:
        raise HTTPException(status_code=404,detail="cart not found")
    prods = json.loads(cart.products)
    found : bool = False
    for item in prods:
        if item["product_id"] == product_id:
            found = True
            if item["amount"]+amount < 0:
                raise HTTPException(status_code=400,detail="Wrong value")
            item["amount"]+=amount
            item["price"]+=amount*product.price
    if amount < 0 and found == False :
        raise HTTPException(status_code=400,detail="Wrong value")
    if found == False:
        prods.append({"product_id":product_id,"amount":amount,"price":amount*product.price})
    prods = json.dumps(prods)
    cart.products = prods
    cart.total =cart.total+ amount*product.price
    db.add(cart)
    db.commit()
    return {
        "status":"success",
        "products":cart.products,
        "total":cart.total
    }

