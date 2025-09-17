import sys
from pathlib import Path
from celery import Celery

# Add the project root directory to sys.path
project_root = Path(__file__).resolve().parent
# First find tasks.py in root directory
sys.path.insert(0, str(project_root))

app = Celery("tasks", broker="redis://localhost:6379/0")
# app = Celery("tasks", broker="redis://redis:6379/0")

# Searches for tasks in the tasks.py file
app.autodiscover_tasks(["tasks"])

app.conf.beat_schedule = {
    "fetch-users-every-5-minutes": {
        "task": "tasks.fetch_and_save_users_task",
        "schedule": 10,  # 10 seconds
    },
}
