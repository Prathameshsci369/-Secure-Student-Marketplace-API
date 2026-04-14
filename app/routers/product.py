from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from pathlib import Path
import aiofiles

# Absolute Imports (Crucial for your structure)
from app.database import get_db
from app.models import Product, User
from app.schemas import Product as ProductSchema
from app.auth import get_current_user

router = APIRouter()

# --- CONFIGURATION ---
# Define where files are stored
UPLOAD_DIR = "uploads"
# Ensure the directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Whitelist for security (Prevent .exe, .sh uploads)
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

def is_safe_file(filename: str) -> bool:
    """Checks if the file extension is allowed."""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

# --- 1. UPLOAD PRODUCT ENDPOINT ---
@router.post("/upload", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def upload_product(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # User must be logged in
):
    # 1. Security Check: File Type
    if not is_safe_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF, JPG, PNG allowed."
        )

    # 2. Sanitize Filename (Prevent directory traversal attacks)
    # We use UUID so no two files have the same name
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_location = os.path.join(UPLOAD_DIR, unique_filename)

    # 3. Save File to Disk (Async)
    try:
        async with aiofiles.open(file_location, 'wb') as out_file:
            # Read file in chunks to prevent memory overload on large files
            content = await file.read()
            await out_file.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {str(e)}"
        )

    # 4. Save Metadata to Database
    new_product = Product(
        title=title,
        description=description,
        price=price,
        file_path=file_location,
        seller_id=current_user.id,
        is_approved=False # Requires admin approval later
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product

# --- 2. LIST ALL PRODUCTS ENDPOINT ---
@router.get("/", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    """
    Returns list of all uploaded notes.
    (In a real app, you might want to filter by is_approved=True)
    """
    products = db.query(Product).all()
    return products

# --- 3. GET SINGLE PRODUCT ENDPOINT ---
@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product