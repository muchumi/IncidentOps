from pydantic import BaseModel, EmailStr, ConfigDict

# Creating Pydantic models to validate request and response data

# Request body for creating a new user
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

