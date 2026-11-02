from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC


"""
    Defining the JWT configuration.
    Configuration variables used when generating your access token.
    This code creates a JWT (JSON Web Token) access token that can be used to authenticate users in IncidentOps API.
"""
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Calculating the expiration time for the access token
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adding the expiration time to the token data
    to_encode.update({"exp": expire})
    
    # Encoding the JWT with the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

