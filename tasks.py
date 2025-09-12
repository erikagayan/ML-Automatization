from celery_app import app
from services.api_service import fetch_users
from services.csv_service import save_users_to_csv
import logging

logger = logging.getLogger(__name__)

@app.task
def fetch_and_save_users_task():
    """
    Celery task to fetch users from API and save to CSV.
    """
    try:
        users = fetch_users()
        save_users_to_csv(users, filename="/app/users.csv")
        logger.info("Users fetched and saved to /app/users.csv")
    except Exception as e:
        logger.error(f"Task failed: {e}")
        raise

if __name__ == "__main__":
    try:
        fetch_and_save_users_task()
        print("Task executed successfully")
    except Exception as e:
        print(f"Error executing task: {e}")