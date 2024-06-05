import sys
sys.path.append("..")
from fastapi import Depends, APIRouter, status, Query
from sqlalchemy.orm import Session
from database import get_db

from models.instances import CreateProduct
from controllers.productController import create_product, get_all_product_handler, getProduct_handler, delete_product_handler

router = APIRouter(
    prefix = "/product",
    tags = ["product"]
)

@router.post("/", status_code = status.HTTP_201_CREATED)
async def create_product_handler(product: CreateProduct, db: Session = Depends(get_db)):
    return await create_product(product, db)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_product(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page numebr"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based title of products")
):
    return await get_all_product_handler(db, page, limit, search)


@router.get('/{product_id}', status_code=status.HTTP_200_OK)
async def getProduct(product_id: int, db: Session = Depends(get_db)):
    return await getProduct_handler(product_id, db)

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    return await delete_product_handler(db, product_id)

