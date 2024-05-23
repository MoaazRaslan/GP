from fastapi import FastAPI , Depends
from models import schemas
from database import engine , SessionLocal
from sqlalchemy.orm import session
from routers import auth

app = FastAPI()
app.include_router(auth.router)
schemas.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/getAll")
async def get_user(db : session = Depends(get_db)):
    return db.query(schemas.User).all()
