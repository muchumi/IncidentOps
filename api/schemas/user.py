from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Creating Pydantic models to validate request and response data

# Request body for creating a new user
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


# Response model for returning user data (does not include password for security reasons)
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    profile_picture: Optional[str]=None
    # required to return SQLAlchemy models inform of JSON response
    model_config = ConfigDict(from_attributes=True)