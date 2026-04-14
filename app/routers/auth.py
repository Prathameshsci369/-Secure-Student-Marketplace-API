from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session 
from app.database import get_db 
from app.models import User 
from app.schemas import UserCreate, User as UserSchema 
from app.auth import verify_password, get_password_hash, create_access_token,get_current_user
router = APIRouter()

@router.post("/register", response_model= UserSchema, status_code= status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 



#--login endpoint
@router.post("/login")
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authentication": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id
    }

@router.get("/me", response_model = UserSchema)
def read_users_me(current_user = Depends(get_current_user)):
    return current_user