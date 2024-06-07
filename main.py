from fastapi import FastAPI, Depends
from models import schemas
from database import engine , get_db
from sqlalchemy.orm import session
from routers import authRouter, productsRouter , profileRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
       "http://localhost:5173", 
   ]

app.add_middleware(
       CORSMiddleware,
       allow_origins=origins,
       allow_credentials=True,
       allow_methods=["*"],     
       allow_headers=["*"],     
   )


app.include_router(authRouter.router)
app.include_router(productsRouter.router)
app.include_router(profileRouter.router)
schemas.Base.metadata.create_all(bind=engine)

@app.get("/getAll")
async def get_user(db : session = Depends(get_db)):
    return db.query(schemas.User).all()
