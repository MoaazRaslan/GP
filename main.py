from fastapi import FastAPI, Depends
from models import schemas
from database import engine , get_db
from sqlalchemy.orm import session
from routers import authRouter, productsRouter , profileRouter , cartRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()

origins = [
       "http://localhost:5173", 
   ]

app.add_middleware(SessionMiddleware, secret_key="add any string...")
app.add_middleware(
       CORSMiddleware,
       allow_origins="*",
       allow_credentials=True,
       allow_methods=["*"],     
       allow_headers=["*"],     
   )


app.include_router(authRouter.router)
app.include_router(productsRouter.router)
app.include_router(profileRouter.router)
app.include_router(cartRouter.router)
schemas.Base.metadata.create_all(bind=engine)

@app.get("/getAll")
async def get_user(db : session = Depends(get_db)):
    return db.query(schemas.User).all()
@app.get("/check")
async def nn(db : session = Depends(get_db)):
    return db.query(schemas.User).filter(schemas.User.id == 2).firlst
