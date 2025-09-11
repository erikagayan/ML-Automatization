from fastapi import FastAPI
from routers import tasks_routers
from tasks import fetch_and_save_users_task

app = FastAPI()
app.include_router(tasks_routers.router)

@app.post("/trigger-fetch")
async def trigger_fetch():
    """
    Trigger the Celery task to fetch users and save to CSV.
    """
    fetch_and_save_users_task.delay()
    return {"message": "Task triggered successfully"}