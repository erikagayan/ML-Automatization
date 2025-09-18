from uuid import UUID
from typing import Sequence
from sqlalchemy import select
from database.models import Task
from schemas import TaskCreate, TaskUpdate
from sqlalchemy.ext.asyncio import AsyncSession


async def get_task_by_id(db: AsyncSession, task_id: UUID) -> Task | None:
    return await db.get(Task, task_id)

async def get_tasks(db: AsyncSession) -> Sequence[Task]:
    result = await db.execute(select(Task))
    return result.scalars().all()

async def create_task(db: AsyncSession, task: TaskCreate) -> Task:
    db_task = Task(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_task(db: AsyncSession, task_id: UUID, task_update: TaskUpdate) -> Task | None:
    db_task = await get_task_by_id(db, task_id)
    if db_task:
        for attr, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, attr, value)
        await db.commit()
        await db.refresh(db_task)
    return db_task

async def delete_task(db: AsyncSession, task_id: UUID) -> Task | None:
    db_task = await get_task_by_id(db, task_id)
    if db_task:
        await db.delete(db_task)
        await db.commit()
    return db_task
