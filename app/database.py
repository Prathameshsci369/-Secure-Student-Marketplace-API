from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
import os 

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:your_password@localhost/student_marketplace"

SQLALCHEMY_DATABASE_URL = "postgresql://marketplace_user:12345@localhost:5432/student_marketplace"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()


