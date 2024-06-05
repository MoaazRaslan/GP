from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from models import schemas
from models.instances import CreateProduct


async def create_product(product: CreateProduct, db: Session):
    newProduct = schemas.Product()
    newProduct.title = product.title
    newProduct.name = product.name
    newProduct.photo = product.photo
    newProduct.price = product.price
    newProduct.description = product.description
    newProduct.amount = product.amount
    newProduct.category = product.category
    newProduct.tags = product.tags
    print(newProduct)
    db.add(newProduct)
    db.commit()
    return {
        "status": "success",
        "data": {
            "title": newProduct.title,
            "name": newProduct.name,
            "photo": newProduct.photo,
            "price": newProduct.price,
            "description": newProduct.description,
            "amount": newProduct.amount,
            "category": newProduct.category,
            "tags": newProduct.tags,
        }
    }


async def get_all_product_handler(db: Session, page: int, limit: int, search: str = ""):
    products = db.query(schemas.Product).order_by(schemas.Product.id.asc()).filter(
        schemas.Product.title.contains(search)).limit(limit).offset((page - 1) * limit).all()
    return {
        "status": "success",
        "result": len(products),
        "data": products
    }

async def getProduct_handler(product_id: int, db: Session):
    product = db.query(schemas.Product).filter(schemas.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid ID')
    return {
        "status": "success",
        "data": product
    }

async def delete_product_handler(db: Session, product_id: int):
    db_product = db.query(schemas.Product).filter(schemas.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid ID')
    db.delete(db_product)
    db.commit()
    return {
        "status": "sucess",
    }


async def update_product_handler(db: Session, product_id: int, updated_product: CreateProduct):
    db_product = db.query(schemas.Product).filter(schemas.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid product's ID")

    for key, value in updated_product.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return {
        "status": "sucess",
        "data": db_product
    }
