
from sqlalchemy import (Column,Integer,String,Text,ForeignKey,DateTime)
from sqlalchemy.sql import func
from api.db.database import Base

class Task(Base):
    __tablename__ = "tasks"
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    # Ticket information
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    # Ticket classification
    priority = Column(String(20), default="MEDIUM", nullable=False)
    status = Column(String(30), default="OPEN", nullable=False)
    # Ticket ownership and assignment
    created_by = Column(Integer,ForeignKey("users.id"),nullable=False)
    assigned_to = Column(Integer,ForeignKey("users.id"),nullable=True)
    # Timestamps
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
