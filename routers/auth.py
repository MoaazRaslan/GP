from fastapi import FastAPI, Depends, HTTPException,APIRouter,status
from pydantic import BaseModel
from models import schemas
from passlib.context import CryptContext
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from decouple import config

SECRET_KEY = "MEZOOO"
ALGORITH = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

class CreateUser(BaseModel):
    user_name: str
    email: str
    password: str
    first_name :str
    last_name :str
    photo :str
    address :str

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

schemas.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={401:{"user":"Not authurized"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def create_access_token(user, expire_delta: Optional[timedelta] = None):
    if not expire_delta:
        expire_delta = timedelta(minutes=15)
    exp = datetime.utcnow() + expire_delta
    encoded = {
        "user_name":user.user_name,
        "id":user.id,
        "email":user.email,
        "address":user.address,
        "first_name":user.first_name,
        "last_name":user.last_name,
        "photo":user.photo,
        "exp": exp
    }
    return jwt.encode(encoded, config("SECRET_KEY"), config("ALGORITHM"))


def get_information_token(token: str = Depends(oauth2_bearer)):
    try:
        user = jwt.decode(token, config("SECRET_KEY"), config("ALGORITHM"))
        user_name = user.get("sub")
        user_id = user.get("id")
        if user_name is None or user_id is None:
            raise HTTPException(status_code=404, detail="User not found !")
        return {"user_name": user_name, "user_id": user_id}
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

@router.post("/sign_up",status_code=201)
async def create_user(cur: CreateUser, db: Session = Depends(get_db)):
    newUser = schemas.User()
    newUser.user_name = cur.user_name
    newUser.first_name = cur.first_name
    newUser.email = cur.email
    newUser.last_name = cur.last_name
    newUser.photo = cur.photo
    newUser.address = cur.address
    hashed_password = get_password_hash(cur.password)
    newUser.hashed_password = hashed_password
    db.add(newUser)
    db.commit()
    token = create_access_token(newUser,timedelta(minutes=20))
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





@router.post("/log_in",status_code=200)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if not verify_user(form_data.username, form_data.password, db):
        raise HTTPException(status_code=404, detail="User not found !")
    user = db.query(schemas.User).filter(schemas.User.user_name == form_data.username).first()
    token = create_access_token(user, timedelta(minutes=20))
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
@router.get("/get_user")
async def extract_info(user_info : dict = Depends(get_information_token)):
    return user_info

