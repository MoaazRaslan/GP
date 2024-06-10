import sys
sys.path.append("..")
from fastapi import Depends, APIRouter, status, Query
from sqlalchemy.orm import Session
from database import get_db

from models.instances import CreateProduct, UpdateProduct
from controllers.productController import create_product, get_all_products, getProduct, delete_product, update_product, rate_product
from controllers.authcontroller import oauth2_bearer

router = APIRouter(
    prefix = "/product",
    tags = ["product"]
)

@router.post("/", status_code = status.HTTP_201_CREATED)
async def create_product_handler(product: CreateProduct, db: Session = Depends(get_db), token :str = Depends(oauth2_bearer)):
    return await create_product(product, db, token)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_product_handler(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page numebr"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based title of products"), 
    money: int = Query(None, ge=0, description="filtering by less price"), 
    amount: int = Query(None, ge=1, description="amount of items"), 
    category: str = Query(None, description="filter by category"), 
    tags: list = []
):
    return await get_all_products(db, page, limit, search, money, amount, category, tags)


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_handler(product_id: int, db: Session = Depends(get_db)):
    return await getProduct(product_id, db)


@router.put('/{product_id}', status_code=status.HTTP_200_OK)
async def update_product_handler(product_id: int, product: UpdateProduct, db: Session = Depends(get_db), token :str = Depends(oauth2_bearer)):
    return await update_product(db, product_id, product, token)

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product_handler(product_id: int, db: Session = Depends(get_db), token :str = Depends(oauth2_bearer)):
    return await delete_product(db, product_id, token)

@router.post('/rateProduct/{product_id}', status_code=status.HTTP_200_OK)
async def rate_product_handler(product_id: int, number_stars: int, db: Session = Depends(get_db), token :str = Depends(oauth2_bearer)):
    return await rate_product(db, product_id, number_stars, token)