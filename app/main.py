from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
from app.database import engine, Base
from .routers import auth, product

Base.metadata.create_all(bind=engine)

app=FastAPI(title="secure Student Marketplace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_credentials = True, 
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(product.router, prefix="/api/products", tags=["Poducts"])

@app.get("/")
def read_root():
    return {"message": "Secure Marketplace API is Running"}

