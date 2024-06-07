from fastapi import APIRouter,HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json
from authcontroller import get_user_from_token
from models import schemas


async def create_cart(db : Session ,token : str):
    user = get_user_from_token(db,token)
    order = schemas.Order()
    order.created_at = datetime.utcnow()
    user.cart_id = order.id
    db.add(user)
    db.add(order)
    db.commit()
    return {
        "status":"success"
    }


async def end_cart(db : Session, token: str):
    user = get_user_from_token(db,token)
    order = db.query(schemas.Order).filter(schemas.Order.id == user.cart_id).first()
    if order is None :
        raise HTTPException(status_code=404,detail="Cart not found")
    order.done = True
    user.cart_id = 0
    db.add(user)
    db.add(order)
    db.commit()
    return {
        "status":"success"
    }

async def add_element_to_cart(db : Session,token: str,product_id,amount:int):
    user = get_user_from_token(db,token)
    order = db.query(schemas.Order).filter(schemas.Order.id == user.cart_id).first()
    product = db.query(schemas.Product).filter(schemas.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    if order is None:
        raise HTTPException(status_code=404,detail="order not found")
    prods = json.loads(order.products)
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
    order.products = prods
    db.add(order)
    db.commit()
    return {
        "status":"success"
    }
