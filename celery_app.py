from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")

app.conf.beat_schedule = {
    'fetch-users-every-5-minutes': {
        'task': 'tasks.fetch_and_save_users_task',
        'schedule': 10,  # 10 seconds
    },
}