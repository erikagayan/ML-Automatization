from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
import crud
import schemas
from dependencies import get_db
from joblib import load
from pydantic import BaseModel
from tasks import fetch_and_save_users_task

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[schemas.TaskResponse], operation_id="get_tasks")
async def get_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await crud.get_tasks(db)
    return tasks

@router.post("/", response_model=schemas.TaskResponse, operation_id="create_task")
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db, task)

@router.put("/{task_id}", response_model=schemas.TaskResponse, operation_id="update_task")
async def update_task(task_id: UUID, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    updated_task = await crud.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", operation_id="delete_task")
async def delete_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    deleted_task = await crud.delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

class PredictInput(BaseModel):
    task_description: str

@router.post("/predict")
async def predict_priority(task: PredictInput):
    """
    Predict task priority (high/low) using the trained ML model.
    """
    model = load("ml/model.joblib")
    prediction = model.predict([task.task_description])[0]
    return {"predicted_priority": prediction}

@router.post("/trigger-fetch")
async def trigger_fetch():
    """
    Trigger the Celery task to fetch users from an API and save to CSV.
    """
    task = fetch_and_save_users_task.delay()
    return {"message": "Task triggered successfully", "task_id": task.id}