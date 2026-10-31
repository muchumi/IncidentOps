from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.schemas.task import TaskCreate, TaskResponse
from api.dependencies import get_current_user
from api.models.user import User
from api.models.task import Task


router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Creating a support ticket
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data:TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Logic to create a task
    new_task=Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status="OPEN",
        created_by=current_user.id 
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Getting all tasks submitted by the authenticated user
@router.get("/my-tasks", response_model=list[TaskResponse])
def get_my_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = (db.query(Task).filter(Task.created_by==current_user.id).all())
    return tasks