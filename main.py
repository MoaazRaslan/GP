from fastapi import FastAPI , Depends
from models import schemas
from database import engine , get_db
from sqlalchemy.orm import session
from routers import authRouter, productsRouter

app = FastAPI()
app.include_router(authRouter.router)
app.include_router(productsRouter.router)
schemas.Base.metadata.create_all(bind=engine)

@app.get("/getAll")
async def get_user(db : session = Depends(get_db)):
    return db.query(schemas.User).all()
