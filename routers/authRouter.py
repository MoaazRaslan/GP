from fastapi import  Depends, APIRouter,status
from models import schemas
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models.instances import CreateUser
from controllers.authcontroller import sign_up_handler,sign_in_handler,changerole,oauth2_bearer
schemas.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={401:{"user":"Not authurized"}}
)

@router.post("/signup",status_code=status.HTTP_200_OK)
async def sign_up(cur: CreateUser,db : Session = Depends(get_db)):
    return await sign_up_handler(cur, db)

@router.post("/login",status_code=status.HTTP_200_OK)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await sign_in_handler(db,form_data)

@router.post("/changerole/{second_user_id}",status_code=status.HTTP_200_OK)
async def change_role(second_user_id,token: str = Depends(oauth2_bearer),db : Session = Depends(get_db)):
    info = await changerole(db,second_user_id,token)
    if info.get("message") is None:
        return "NOOOOOOOOOOO"
    return "done"

# @router.get("/get_user")
# async def extract_info(user_info : dict = Depends(get_information_token)):
#     return user_info

