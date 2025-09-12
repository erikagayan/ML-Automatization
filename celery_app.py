import os
import sys
from celery import Celery

# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# app = Celery("tasks", broker="redis://localhost:6379/0")
app = Celery("tasks", broker="redis://redis:6379/0")

# Optionally, keep autodiscover for other tasks
app.autodiscover_tasks(['tasks'])

app.conf.beat_schedule = {
    'fetch-users-every-5-minutes': {
        'task': 'tasks.fetch_and_save_users_task',
        'schedule': 30,  # 10 seconds
    },
}