from sqlalchemy.orm import Session

from models import schemas
from models.instances import CreateProduct


async def create_product(product: CreateProduct, db: Session):
    newProduct = schemas.Product()
    # Mohammad is here