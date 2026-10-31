
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal
from datetime import datetime


# Schema for creating a support ticket
class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Short title describing the IT support request"
    )

    description: str = Field(
        ...,
        min_length=10,
        description="Detailed explanation of the IT issue or support required"
    )

    priority: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "MEDIUM"


# Schema for returning a support ticket
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    created_by: int
    assigned_to: int | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
