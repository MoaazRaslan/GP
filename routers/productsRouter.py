from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Sessoin
from database import get_db

from models.instances import CreateProduct
from controllers.productController import create_product

router = APIRouter(
    prefix = "/product",
    tags = ["product"]
)

router.post("/", status_code = status.HTTP_201_CREATED)
async def create_product_handler(product: CreateProduct, db: Sessoin = Depends(get_db)):
    return create_product()