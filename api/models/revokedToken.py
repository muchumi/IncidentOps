from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from api.db.database import Base

# Model for storing revoked JWT access tokens
class RevokedToken(Base):
    __tablename__ = "revoked_tokens"
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    # Unique identifier of the revoked JWT
    jti = Column(String, unique=True, nullable=False, index=True)
    # Expiration time of the original JWT
    expires_at = Column(DateTime(timezone=True), nullable=False)
    # Date and time when the token was revoked
    revoked_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
