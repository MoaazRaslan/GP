from fastapi import  Depends, APIRouter
from models import schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models.instances import CreateUser
from controller.auth import signup,signin
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


@router.post("/sign_up",status_code=201)
async def sign_up(cur: CreateUser,db : Session = Depends(get_db)):
    info = await signup(cur,db)
    return info

@router.post("/log_in",status_code=200)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    info = await signin(db,form_data)
    return info


# @router.get("/get_user")
# async def extract_info(user_info : dict = Depends(get_information_token)):
#     return user_info

