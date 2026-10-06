from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.main import app
from api.db.database import get_db
from api.core.security import hash_password, verify_password
from api.auth import create_access_token
from api.schemas.user import UserCreate
from api.schemas.TokenResponse import TokenResponse
from api.models.user import User

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # normalize the email to lowercase and strip any leading/trailing whitespace
    normalized_email=user.email.strip().lower()
    # Checking if the user already exists in the database
    existing_user=db.query(User).filter(User.email==normalized_email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    # Hashing the password before storing it in the database
    hashed_password = hash_password(user.password.strip())
    new_user=User(first_name=user.first_name.strip(), last_name=user.last_name.strip(), email=normalized_email, password=hashed_password)
    db.add(new_user)
    db.flush()
    db.commit()
    db.refresh(new_user)
    return new_user()


# User login route
@app.post("/auth/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # normalizing email
    user_email=form_data.username.strip().lower()
    # fetch user from database
    user = db.query(User).filter(User.email == user_email).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(user.email)})
    return TokenResponse(access_token=access_token, token_type="bearer")
    
    
    
    
    
    