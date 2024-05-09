from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY_DATABASE_URL ="sqlite:///./schemas.db"

engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)



Base = declarative_base()