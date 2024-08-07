from datetime import timedelta, datetime
from typing import Optional
from decouple import config
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.requests import Request
from starlette.responses import RedirectResponse

from models import schemas
from models.instances import CreateUser

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id="185911706041-f1k4encstovl4olt4d9o4u9sev2v41po.apps.googleusercontent.com",
    client_secret="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",
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)

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

def get_user_from_token(db : Session,token: str = Depends(oauth2_bearer)):
    info = get_information_token(token)
    user = db.query(schemas.User).filter(schemas.User.id == info.get("user_id")).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return user

def get_admin_info(db : Session,token: str = Depends(oauth2_bearer)):
    info = get_information_token(token)
    user = db.query(schemas.User).filter(schemas.User.id == info.get("user_id")).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    if user.role != 1:
        raise HTTPException(status_code=403,detail="You need to be an admin")
    return user

#same above but i dont need return user, i need this for conditionally render the add product button if the user is an admin 
def check_admin(db : Session,token: str = Depends(oauth2_bearer)):
    info = get_information_token(token)
    user = db.query(schemas.User).filter(schemas.User.id == info.get("user_id")).first()
    if user is None:
        return False
    if user.role != 1:
        return False
    if user.role == 1 :
        return True


def get_information_token(token: str = Depends(oauth2_bearer)):
    try:
        user = jwt.decode(token, config("SECRET_KEY"), config("ALGORITHM"))
        user_id = user.get("id")
        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found !")
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="User not found !")


def verify_user(username, password, db):
    user = db.query(schemas.User) \
        .filter(schemas.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True

def refresh_token(db : Session ,token : str = Depends(oauth2_bearer)):
    info = get_information_token(token)
    user = db.query(schemas.User).filter(schemas.User.id == info.get("user_id")).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    refreshed_token = create_access_token(info.get("user_id"))
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
    return {
        'status': 'success'
        }


async def sign_up(cur: CreateUser, db: Session):
    newUser = schemas.User()
    newUser.username = cur.username
    newUser.first_name = cur.first_name
    newUser.email = cur.email
    newUser.last_name = cur.last_name
    newUser.photo = cur.photo
    newUser.address = cur.address
    newUser.hashed_password = None
    if cur.authType == 1:
        hashed_password = get_password_hash(cur.password)
        newUser.hashed_password = hashed_password

    newUser.role = 0
    # validation and  error handling
    db.add(newUser)
    db.commit()
    token = create_access_token(newUser.id)
    return {
        'status': 'success',
        'token': token,
        'data': {
            "username": newUser.username,
            "email": newUser.email,
            "address": newUser.address,
            "first_name": newUser.first_name,
            "last_name": newUser.last_name,
            "photo": newUser.photo
        }
    }
    
async def sign_in(db: Session, form_data: OAuth2PasswordRequestForm = Depends()):
    if not verify_user(form_data.username, form_data.password, db):
        raise HTTPException(status_code=404, detail="User not found !")
    user = db.query(schemas.User).filter(schemas.User.username == form_data.username).first()
    token = create_access_token(user.id)
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
        }
    }
    
async def oauth_sign_in(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


async def oauth_callback(request: Request, db: Session):
    try:
        googleToken = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print("[[[auth error! ]]]\n", e)
        return

    userInfo = googleToken.get('userinfo')
    print("oauthUserInfo: ", userInfo)
    user = db.query(schemas.User).filter(
        schemas.User.email == userInfo.get("email")).first()
    if (user):
        token = create_access_token(user.id)
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
            }
        }
    else:
        print("user not exsisit!!!")
        newUser = schemas.User()
        newUser.username = userInfo.get("given_name")
        newUser.first_name = userInfo.get("given_name")
        newUser.email = userInfo.get("email")
        newUser.last_name = userInfo.get("family_name")
        newUser.photo = userInfo.get("picture")
        newUser.address = "Aleppo"
        newUser.authType = 2
        newUser.role = 0
        print("newUserInfo))) ", newUser.email)
        sign_up_response = await sign_up(newUser, db)

        return sign_up_response
