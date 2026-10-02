from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from api.main import app
from api.db.database import get_db
from api.core.security import hash_password
from api.schemas.user import UserCreate
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
    
    
    
    
    
    