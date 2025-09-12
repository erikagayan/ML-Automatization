# ML-Automatization

## Overview

A simple FastAPI app for managing tasks with PostgreSQL, SQLAlchemy (async), and Alembic. Supports CRUD operations: create, read, update, and delete tasks. Includes a Celery task to fetch user data from an API and save it to a CSV file, and a machine learning model to predict task priority (high/low) based on task descriptions.

## Tech Stack
- FastAPI
- SQLAlchemy (async with asyncpg)
- PostgreSQL
- Alembic
- Pydantic
- Celery
- Redis
- Requests
- Scikit-learn
- Pandas
- Joblib

## Setup
1. **Clone the repo**:
   ```bash
   git clone https://github.com/erikagayan/ML-Automatization.git
   cd ML-Automatization
   ```

2. **Set up virtual environment** (optional for local development):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies** (optional for local development):
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL** (required for CRUD operations):
   - Create database:
     ```bash
     createdb -U admin -h localhost ml_automatization
     ```
   - Or in pgAdmin 4: Create database `ml_automatization` with owner `admin` (password: `admin`).

5. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Set up Redis** (required for Celery, optional if using Docker):
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

## Running Locally
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
   - Note: PostgreSQL runs locally (not in Docker). Ensure it is set up as described in **Setup**.

3. **Access services**:
   - **FastAPI**: Open `http://127.0.0.1:8000/docs` to access Swagger UI.
   - **Celery Worker**: Processes tasks triggered via `/tasks/trigger-fetch` or scheduled every 5 minutes.
   - **Redis**: Runs on port 6379 (used internally by Celery).

4. **Stop containers**:
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

## Machine Learning Integration
1. **Train the ML model** (predicts task priority: high/low):
   - Run locally:
     ```bash
     python ml/train_model.py
     ```
   - Run in Docker:
     ```bash
     docker-compose exec web python /app/ml/train_model.py
     ```
   - This creates `ml/model.joblib` using `data/tasks.csv`. Expected output:
     ```
     Loaded 16 tasks from data/tasks.csv
     Train set size: 12, Test set size: 4
     Model trained and saved to ml/model.joblib
     Model accuracy on test data: 0.75
     ...
     ```

2. **Verify model file**:
   - Check that `ml/model.joblib` exists:
     ```bash
     ls -l ml/model.joblib
     ```

## Testing
### FastAPI Endpoints
Use Swagger UI (`http://127.0.0.1:8000/docs`) to test:
- **GET /tasks**: List all tasks stored in PostgreSQL.
- **POST /tasks**: Create a task. Example:
  ```json
  {
    "title": "Test Task",
    "description": "Test",
    "completed": false
  }
  ```
- **PUT /tasks/{task_id}**: Update a task by UUID.
- **DELETE /tasks/{task_id}**: Delete a task by UUID.
- **POST /tasks/trigger-fetch**: Trigger the Celery task to fetch users from an API and save to `users.csv`. Example response:
  ```json
  {
    "message": "Task triggered successfully",
    "task_id": "some-uuid"
  }
  ```
- **POST /tasks/predict**: Predict task priority (high/low) based on task description. Example:
  ```json
  {
    "task_description": "Fix login bug on website"
  }
  ```
  Expected response:
  ```json
  {
    "predicted_priority": "high"
  }
  ```

### Celery Task
- **Manual Trigger** (local only):
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
- **Direct Run** (local only, without Celery):
  ```bash
  python tasks.py
  ```

### Testing the ML Model
1. **Verify `/tasks/predict`**:
   - Open `http://127.0.0.1:8000/docs` and find `POST /tasks/predict`.
   - Send a request with:
     ```json
     {
       "task_description": "Fix login bug on website"
     }
     ```
   - Expected response:
     ```json
     {
       "predicted_priority": "high"
     }
     ```
   - Try another task:
     ```json
     {
       "task_description": "Update documentation"
     }
     ```
     Expected response:
     ```json
     {
       "predicted_priority": "low"
     }
     ```
   - Alternatively, use `curl`:
     ```bash
     curl -X POST "http://127.0.0.1:8000/tasks/predict" -H "Content-Type: application/json" -d '{"task_description": "Fix login bug on website"}'
     ```

2. **Troubleshooting `/tasks/predict`**:
   - If you get `FileNotFoundError: ml/model.joblib`, run:
     ```bash
     python ml/train_model.py
     ```
   - If predictions are incorrect, check `data/tasks.csv` for enough data (16+ rows recommended).

### Docker Testing
1. **Test Celery Task**:
   - Use `/tasks/trigger-fetch` in Swagger UI.
   - Check `users.csv` in the project root:
     ```bash
     cat users.csv
     ```
   - View Celery Worker logs:
     ```bash
     docker-compose logs celery_worker
     ```
     Expected:
     ```
     celery_worker_1 | Users fetched and saved to /app/users.csv
     ```

2. **Test ML Model**:
   - Use `/tasks/predict` in Swagger UI.
   - If model is missing, train it in Docker:
     ```bash
     docker-compose exec web python /app/ml/train_model.py
     ```

3. **Apply migrations** (for PostgreSQL, local setup):
   ```bash
   alembic upgrade head
   ```
