from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from api.db.database import get_db
from api.models.user import User
from api.models.revokedToken import RevokedToken
from api.auth import SECRET_KEY, ALGORITHM

#This code receives, verifies and uses that JWT to identify the currently authenticated user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Exception raised when credentials cannot be validated
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        # Decode JWT token to retrieve the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract user's email and unique token identifier
        email=payload.get("sub")
        token_id=payload.get("jti")
        
        # validating if the required claims exists
        if email is None or token_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Checking whether the JWT has been revoked
    revoked_token=db.query(RevokedToken).filter(RevokedToken.jti==token_id).first()
    if revoked_token:
        raise credentials_exception 
    # querying the database to get the user with the email from the token
    user = db.query(User).filter(User.email==email).first()
    if user is None:
        raise credentials_exception
    return user  