import csv
import os
from typing import List, Dict

def save_users_to_csv(users: List[Dict], filename: str) -> None:
    """
    Save user data to a CSV file with columns: id, name, email.
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'email'])
        for user in users:
            writer.writerow([user['id'], user['name'], user['email']])

if __name__ == "__main__":
    test_users = [
        {"id": 1, "name": "Test User 1", "email": "test1@example.com"},
        {"id": 2, "name": "Test User 2", "email": "test2@example.com"},
    ]
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "test_users.csv")
        save_users_to_csv(test_users, csv_path)
        print(f"Test data saved to {csv_path}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")