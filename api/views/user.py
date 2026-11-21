from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pathlib import Path
from uuid import uuid4
from io import BytesIO
from PIL import Image
import os

from api.db.database import get_db
from api.core.security import hash_password, verify_password
from api.auth import create_access_token
from api.schemas.user import UserCreate, UserResponse
from api.schemas.TokenResponse import TokenResponse
from api.dependencies import get_current_user
from api.models.user import User


# Directory for storing profile pictures
PROFILE_DIR = Path("static/profile_pictures")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

# Maximum upload size: 5 MB
MAX_FILE_SIZE = 5 * 1024 * 1024

# Supported image formats
ALLOWED_FORMATS = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "WEBP": ".webp"
}

router = APIRouter(prefix="/users", tags=["Users"])

# User registration route
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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
    return new_user


# User login route
@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # normalizing email
    user_email=form_data.username.strip().lower()
    # fetch user from database
    user = db.query(User).filter(User.email == user_email).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(user.email)})
    return TokenResponse(access_token=access_token, token_type="bearer")

# Getting the current user route
@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
      
# Route / endpoint that allows users to update their profile picture
@router.put("/me/profile-picture",status_code=status.HTTP_200_OK)
def update_profile_picture(file: UploadFile = File(...), db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    # Read uploaded file
    file_content = file.file.read(MAX_FILE_SIZE + 1)

    # Validate file size
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image must not exceed 5 MB"
        )

    # Validate that the uploaded file is a genuine image
    try:
        image = Image.open(BytesIO(file_content))
        image.verify()

        image_format = image.format

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file"
        )

    # Check supported image format
    if image_format not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG and WEBP images are allowed"
        )

    # Generate a unique filename
    file_extension = ALLOWED_FORMATS[image_format]
    filename = f"{uuid4().hex}{file_extension}"

    # Save image
    file_path = PROFILE_DIR / filename

    try:
        file_path.write_bytes(file_content)

        # Save image path in database
        old_picture = current_user.profile_picture
        current_user.profile_picture = (
            f"/static/profile_pictures/{filename}"
        )

        db.commit()
        db.refresh(current_user)

    except Exception:
        db.rollback()

        # Remove newly uploaded image if database update fails
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile picture"
        )

    # Remove previous picture after successful update
    if old_picture:
        old_filename = Path(old_picture).name
        old_file = PROFILE_DIR / old_filename

        if old_file.parent == PROFILE_DIR and old_file.exists():
            old_file.unlink()

    return {
        "message": "Profile picture updated successfully",
        "profile_picture": current_user.profile_picture
    }
    

# Endpoint that allows users to delete their profile picture
@router.delete("/me/profile-picture", status_code=status.HTTP_200_OK)
def delete_profile_picture(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    # Check whether the user has a profile picture
    if not current_user.profile_picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You do not have a profile picture"
        )

    # Get the existing profile picture filename
    filename = Path(current_user.profile_picture).name

    # Construct the image path
    file_path = PROFILE_DIR / filename

    # Remove the image from storage
    if file_path.exists() and file_path.is_file():
        file_path.unlink()

    # Remove the image reference from the database
    current_user.profile_picture = None

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile picture deleted successfully",
        "profile_picture": current_user.profile_picture
    }
   
# Endpoint that allows user to log out from their account
@router.post("/logout", status_code=status.HTTP_200_OK)
def user_logout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"message": "You have been logged out successfully"}   