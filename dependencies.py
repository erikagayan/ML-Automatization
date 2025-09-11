from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import SessionLocal
from fastapi import Depends

async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
