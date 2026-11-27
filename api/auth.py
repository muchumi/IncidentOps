from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from uuid import uuid4


"""
    Defining the JWT configuration.
    Configuration variables used when generating your access token.
    This code creates a JWT (JSON Web Token) access token that can be used to authenticate users in IncidentOps API.
"""
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Function for generating JWT access tokens. It takes a dictionary of data as input, adds an expiration time to it, and encodes it using the specified secret key and algorithm.
def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Generate a unique identifier for this token
    token_id=str(uuid4())
    
    # Calculating the expiration time for the access token
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add token identification and expiration information
    to_encode.update({
        "jti": token_id,
        "exp": expire
    })
    
    # Encoding the JWT with the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

