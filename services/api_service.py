import requests
from typing import Dict, List

def fetch_users() -> List[Dict]:
    """
    Fetch users from JSONPlaceholder API.
    Returns a list of user dictionaries.
    """

    response = requests.get("https://jsonplaceholder.typicode.com/users")
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        users = fetch_users()
        print("Fetched users: ")
        for user in users:
            print(f"ID: {user["id"]}, Name: {user["name"]}, Email: {user["email"]}")
    except requests.RequestException as e:
        print(f"Error fetching users: {e}")
