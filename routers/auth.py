from fastapi import  Depends, APIRouter,status
from models import schemas
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models.instances import CreateUser
from controller.auth import signup,signin,changerole,oauth2_bearer
schemas.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={401:{"user":"Not authurized"}}
)

@router.post("/sign_up",status_code=status.HTTP_200_OK)
async def sign_up(cur: CreateUser,db : Session = Depends(get_db)):
    info = await signup(cur,db)
    return info

@router.post("/log_in",status_code=status.HTTP_200_OK)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    info = await signin(db,form_data)
    return info

@router.post("/changerole/{second_user_id}",status_code=status.HTTP_200_OK)
async def change_role(second_user_id,token: str = Depends(oauth2_bearer),db : Session = Depends(
    get_db
)):
    info = await changerole(db,second_user_id,token)
    if info.get("message") is None:
        return "NOOOOOOOOOOO"
    return "done"

# @router.get("/get_user")
# async def extract_info(user_info : dict = Depends(get_information_token)):
#     return user_info

