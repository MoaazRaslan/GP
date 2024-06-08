from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from database import get_db
from models.instances import CreateUser
from controllers.authcontroller import oauth2_bearer
from controllers.cartController import add_element_to_cart, end_cart, get_cart


router = APIRouter(
     prefix="/cart",
    tags=["Cart"],
    responses={401:{"cart":"Not found"}}
)


@router.get("/getCart",status_code=status.HTTP_201_CREATED)
async def create_cart_handler(db : Session = Depends(get_db),token : str = Depends(oauth2_bearer)):
    return await get_cart(db,token)

@router.post("/endCart",status_code=status.HTTP_200_OK)
async def end_cart_handler(db : Session = Depends(get_db),token : str = Depends(oauth2_bearer)):
    return await end_cart(db,token)


@router.post("/addProducttToCart/{product_id}/{amount}",status_code=status.HTTP_201_CREATED)
async def add_element_to_cart_handler(product_id,amount,db : Session = Depends(get_db),token : str = Depends(oauth2_bearer)):
    return await add_element_to_cart(product_id,amount,db,token)


