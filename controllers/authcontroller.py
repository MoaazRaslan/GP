from datetime import timedelta, datetime
from typing import Optional
from decouple import config
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models import schemas
from models.instances import CreateUser

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def create_access_token(user_id):
    de = int(config("TIME_DELTA"))
    expire_delta = timedelta(hours=de)
    exp = datetime.utcnow() + expire_delta
    encoded = {
        "id": user_id,
        "exp": exp
    }
    return jwt.encode(encoded, config("SECRET_KEY"), config("ALGORITHM"))


def get_information_token(token: str = Depends(oauth2_bearer)):
    try:
        user = jwt.decode(token, config("SECRET_KEY"), config("ALGORITHM"))
        user_id = user.get("id")
        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found !")
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="User not found !")


def verify_user(user_name, password, db):
    user = db.query(schemas.User) \
        .filter(schemas.User.user_name == user_name).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True

def refresh_token(token : str = Depends(oauth2_bearer)):
    info = get_information_token(token)
    refreshed_token = create_access_token(info .get("user_id"))
    return refreshed_token


async def changerole(db : Session,second_person_id :int ,token : str = Depends(oauth2_bearer)):
    info = get_information_token(token)
    id = info.get("user_id")
    if id is None:
        raise HTTPException(status_code=404,detail="User not found!")
    user = db.query(schemas.User).filter(id == schemas.User.id).first()
    second_person = db.query(schemas.User).filter(second_person_id == schemas.User.id).first()
    if user is None or second_person is None:
        raise HTTPException(status_code=404,detail="User not found!")
    if user.role >= 2:
        second_person.role ^=1
    else:
        raise HTTPException(status_code=403,detail="Unauthorized")
    db.add(second_person)
    db.commit()
    return {"message":"Done"}

async def signup(cur: CreateUser, db: Session ):
    newUser = schemas.User()
    newUser.user_name = cur.user_name
    newUser.first_name = cur.first_name
    newUser.email = cur.email
    newUser.last_name = cur.last_name
    newUser.photo = cur.photo
    newUser.address = cur.address
    hashed_password = get_password_hash(cur.password)
    newUser.hashed_password = hashed_password
    newUser.role = 0
    db.add(newUser)
    db.commit()
    token = create_access_token(newUser.id)
    user_info = {
        "user_name": newUser.user_name,
        "email": newUser.email,
        "address": newUser.address,
        "first_name": newUser.first_name,
        "last_name": newUser.last_name,
        "photo": newUser.photo,
    }
    return {
        'token': token,
        'user_info': user_info
    }

async def signin(db: Session, form_data: OAuth2PasswordRequestForm = Depends()):
    if not verify_user(form_data.username, form_data.password, db):
        raise HTTPException(status_code=404, detail="User not found !")
    user = db.query(schemas.User).filter(schemas.User.user_name == form_data.username).first()
    token = create_access_token(user.id)
    user_info = {
        "user_name": user.user_name,
        "email": user.email,
        "address": user.address,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "photo": user.photo,
    }
    return {
        'token': token,
        'user_info':user_info
    }