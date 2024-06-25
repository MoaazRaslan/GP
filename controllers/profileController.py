from fastapi import HTTPException
from sqlalchemy.orm import session
from controllers.authcontroller import get_information_token,create_access_token
from models import schemas,instances

def get_info_handler(db: session,token :str):
    info = get_information_token(token)
    user = db.query(schemas.User).filter(schemas.User.id == info.get("user_id")).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User Not Found")
    return {
        'status': 'success',
        'token': token,
        'data': {
            "username": user.username,
            "email": user.email,
            "address": user.address,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "photo": user.photo,
            "role" : user.role
        }   
    }

def edit_info_handler(updated_info : instances.CreateUser,db: session,token :str):
    info = get_information_token(token)
    user = db.query(schemas.User).filter(schemas.User.id == info.get("user_id")).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User Not Found")
    user.first_name = updated_info.first_name
    user.email = updated_info.email
    user.last_name = updated_info.last_name
    user.photo = updated_info.photo
    user.address = updated_info.address
    db.add(user)
    db.commit()
    token = create_access_token(user.id)
    print(user.email)
    return {
        'status': 'success',
        'token': token,
        'data': {
            "username": user.username,
            "email": user.email,
            "address": user.address,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "photo": user.photo
        }   
    }


def delete_user_handler(db: session,token :str):
    info = get_information_token(token)
    user = db.query(schemas.User).filter(schemas.User.id == info.get("user_id")).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User Not Found")
    db.delete(user)
    db.commit()
    return {
        'status': 'success', 
    }