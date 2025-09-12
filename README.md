# ML-Automatization

## Overview

A simple FastAPI app for managing tasks with PostgreSQL, SQLAlchemy (async), and Alembic. Supports CRUD operations: create, read, update, and delete tasks. Additionally, it includes a Celery task to fetch user data from an API and save it to a CSV file.

## Tech Stack
- FastAPI
- SQLAlchemy (async with asyncpg)
- PostgreSQL
- Alembic
- Pydantic
- Celery
- Redis
- Requests

## Setup
1. **Clone the repo**:
   ```bash
   git clone https://github.com/erikagayan/ML-Automatization.git
   cd ML-Automatization
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL**:
   - Create database: `createdb -U admin -h localhost ml_automatization`
   - Or in pgAdmin 4: Create database `ml_automatization` with owner `admin` (password: `admin`).

5. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Set up Redis** (required for Celery):
   - Install Redis:
     ```bash
     brew install redis  # macOS
     # or
     sudo apt install redis-server  # Linux
     ```
   - Start Redis:
     ```bash
     redis-server
     ```
   - Verify Redis is running:
     ```bash
     redis-cli ping  # Should return "PONG"
     ```

## Running
1. **Activate virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Start the FastAPI app**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Open Swagger UI**:
   - Visit `http://127.0.0.1:8000/docs`

4. **Start Celery Worker** (to process tasks):
   ```bash
   celery -A celery_app worker --loglevel=info
   ```

5. **Start Celery Beat** (to schedule tasks every 5 minutes):
   ```bash
   celery -A celery_app beat --loglevel=info
   ```
   
## Running with Docker
1. **Install Docker**:
   - Download and install [Docker Desktop](https://www.docker.com/get-started) for macOS/Windows or Docker for Linux.

2. **Build and start containers**:
   - Run the following command to build and start FastAPI, Celery Worker, and Redis:
     ```bash
     docker-compose up --build
     ```

3. **Access services**:
   - **FastAPI**: Open `http://127.0.0.1:8000/docs` to access Swagger UI.
   - **Celery Worker**: Processes tasks triggered via the `/trigger-fetch` endpoint or scheduled every 5 minutes.
   - **Redis**: Runs on port 6379 (used internally by Celery).

4. **Stop containers**:
   - To stop and remove containers:
     ```bash
     docker-compose down
     ```

5. **View logs**:
   - Check FastAPI logs:
     ```bash
     docker-compose logs web
     ```
   - Check Celery Worker logs:
     ```bash
     docker-compose logs celery_worker
     ```
   - Check Redis logs:
     ```bash
     docker-compose logs redis
     ```



## Testing
### FastAPI Endpoints
Use Swagger UI (`http://127.0.0.1:8000/docs`) to test:
- **GET /tasks**: List all tasks.
- **POST /tasks**: Create a task (e.g., `{"title": "Test Task", "description": "Test", "completed": false}`).
- **PUT /tasks/{task_id}**: Update a task by UUID.
- **DELETE /tasks/{task_id}**: Delete a task by UUID.
- **POST /trigger-fetch**: Trigger the Celery task to fetch users from an API and save to `users.csv`.

### Celery Task
- **Manual Trigger**: Run the Celery task manually:
  ```bash
  python -c "from tasks import fetch_and_save_users_task; fetch_and_save_users_task.delay()"
  ```
- **Check Result**: Verify that `users.csv` is created/updated in the project root:
  ```bash
  cat users.csv
  ```
  Expected output:
  ```
  id,name,email
  1,Leanne Graham,Sincere@april.biz
  2,Ervin Howell,Shanna@melissa.tv
  ...
  ```
- **Direct Run**: Test the task without Celery:
  ```bash
  python tasks.py
  ```