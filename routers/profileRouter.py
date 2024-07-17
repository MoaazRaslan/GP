from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import session
from database import get_db
from models.instances import CreateUser
from controllers.authcontroller import oauth2_bearer,check_admin
from controllers.profileController import get_info_handler,edit_info_handler,delete_user_handler
router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    responses={404:{"user":"Not Found!"}}
)

@router.get("/myprofile",status_code=status.HTTP_200_OK)
async def get_info(db: session = Depends(get_db),token :str = Depends(oauth2_bearer)):
    return get_info_handler(db,token)


@router.put("/editmyprofile",status_code=status.HTTP_200_OK)
async def edit_info(updated_info: CreateUser,db: session = Depends(get_db),token :str = Depends(oauth2_bearer)):
    return edit_info_handler(updated_info,db,token)

@router.delete("/deleteuser",status_code=status.HTTP_200_OK)
async def delete_user(db: session = Depends(get_db),token :str = Depends(oauth2_bearer)):
    return delete_user_handler(db,token)

@router.get("/checkadmin",status_code=status.HTTP_200_OK)
async def check_if_admin(db: session = Depends(get_db),token :str = Depends(oauth2_bearer)):
    return check_admin(db,token)
