from fastapi import FastAPI
from routers import tasks_routers

app = FastAPI()

app.include_router(tasks.router)
