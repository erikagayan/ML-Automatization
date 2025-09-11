from celery_app import app
from services.api_service import fetch_users
from services.csv_service import save_users_to_csv

@app.task
def fetch_and_save_users_task():
    """
    Celery task to fetch users from API and save to CSV.
    """
    users = fetch_users()
    save_users_to_csv(users)
    print("Users fetched and saved to users.csv")

if __name__ == "__main__":
    try:
        fetch_and_save_users_task()
        print("Task executed successfully")
    except Exception as e:
        print(f"Error executing task: {e}")