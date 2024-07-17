from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from models import schemas
from models.instances import CreateProduct, UpdateProduct
from controllers.authcontroller import get_admin_info, get_user_from_token


async def create_product(product: CreateProduct, db: Session, token: str):
    get_admin_info(db, token)
    newProduct = schemas.Product()
    newProduct.title = product.title
    newProduct.photo = product.photo
    newProduct.price = product.price
    newProduct.description = product.description
    newProduct.amount = product.amount
    newProduct.category = product.category
    newProduct.tags = product.tags
    db.add(newProduct)
    db.commit()
    return {
        "status": "success",
        "data": {
            "id": newProduct.id,
            "title": newProduct.title,
            "photo": newProduct.photo,
            "price": newProduct.price,
            "description": newProduct.description,
            "amount": newProduct.amount,
            "category": newProduct.category,
            "tags": newProduct.tags,
        }
    }


async def get_all_products(db: Session, page: int, limit: int, search: str, money: int, amount: int, category: str, tags: list):
    # Start the query with base filters
    query = db.query(schemas.Product).order_by(schemas.Product.average_rate.desc()).filter(
        schemas.Product.title.contains(search)
    )
    
    # Apply additional filters if provided
    if money is not None:
        query = query.filter(schemas.Product.price <= money)
    
    if amount is not None:
        query = query.filter(schemas.Product.amount >= amount)
    
    if category:
        query = query.filter(schemas.Product.category == category)
    
    # if tags:
        # Assuming Product.tags is a relationship that can be checked with `any`
        # If it's a simple array column, adapt accordingly
        # query = query.filter(or_(*[schemas.Product.tags.contains(tag) for tag in tags]))

    # Paginate the results
    products = query.limit(limit).offset((page - 1) * limit).all()
    
    return {
        "status": "success",
        "result": len(products),
        "data": products
    }

async def getProduct(product_id: int, db: Session):
    product = db.query(schemas.Product).filter(schemas.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid ID')
    return {
        "status": "success",
        "data": product
    }

async def delete_product(db: Session, product_id: int, token: str):
    get_admin_info(db, token)
    db_product = db.query(schemas.Product).filter(schemas.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid ID')
    db.delete(db_product)
    db.commit()
    return {
        "status": "success",
    }

async def update_product(db: Session, product_id: int, updated_product: UpdateProduct, token: str):
    get_admin_info(db, token)
    db_product = db.query(schemas.Product).filter(schemas.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid product's ID")

    for key, value in updated_product.model_dump().items():
        if value == None:
            continue
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return {
        "status": "sucess",
        "data": db_product
    }

async def rate_product(db: Session, product_id: int, number_stars: int, token: str):
    user = get_user_from_token(db, token)
    exist = db.query(schemas.Rate).filter(schemas.Rate.product_id == product_id).filter(schemas.Rate.user_id == user.id).first()   
    if exist is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already voted for this product")
    
    newRate = schemas.Rate()
    newRate.product_id = product_id
    newRate.user_id = user.id
    newRate.stars = number_stars
    db.add(newRate)
    db.commit()

    db_product = db.query(schemas.Product).filter(schemas.Product.id == product_id).first()
    db_product.sum_of_stars += number_stars
    db_product.cnt_voter += 1
    db_product.average_rate = 1.0 * db_product.sum_of_stars / db_product.cnt_voter

    db.commit()
    db.refresh(db_product)

    return {
        "status": "success",
        "data": db_product
    }