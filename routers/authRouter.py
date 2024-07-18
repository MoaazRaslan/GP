from starlette.responses import RedirectResponse
from starlette.requests import Request
from fastapi import  Depends, APIRouter,status
from models import schemas
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models.instances import CreateUser
from controllers.authcontroller import sign_up, sign_in, oauth_sign_in, oauth_callback, changerole, oauth2_bearer, refresh_token
schemas.Base.metadata.create_all(bind=engine)

# from authlib.integrations.starlette_client import OAuth, OAuthError

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={401:{"user":"Not authurized"}}
)

@router.post("/signup",status_code=status.HTTP_200_OK)
async def sign_up_handler(cur: CreateUser,db : Session = Depends(get_db)):
    return await sign_up(cur, db)

@router.post("/login",status_code=status.HTTP_200_OK)
async def sign_in_handler(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await sign_in(db,form_data)


@router.get("/oauth-login")
async def oauth_sign_in_handler(request: Request):

    return await oauth_sign_in(request)


@router.get('/auth-callback')
async def auth(request: Request, db: Session = Depends(get_db)):
    return await oauth_callback(request, db)


@router.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse('/')

@router.post("/changerole/{second_user_id}",status_code=status.HTTP_200_OK)
async def change_role(second_user_id,token: str = Depends(oauth2_bearer),db : Session = Depends(get_db)):
    return await changerole(db,second_user_id,token)

@router.post("/refresh",status_code=status.HTTP_200_OK)
async def refresh_access_token(token : str = Depends(oauth2_bearer),db : Session = Depends(get_db)):
    return await refresh_token(db ,token)
# @router.get("/get_user")
# async def extract_info(user_info : dict = Depends(get_information_token)):
#     return user_info

