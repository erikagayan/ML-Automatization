# ML-Automatization

## Overview

A simple FastAPI app for managing tasks with PostgreSQL, SQLAlchemy (async), and Alembic. Supports CRUD operations: create, read, update, and delete tasks.

## Tech Stack
- FastAPI
- SQLAlchemy (async with asyncpg)
- PostgreSQL
- Alembic
- Pydantic

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
   pip install requirements.txt
   ```

4. **Set up PostgreSQL**:
   - Create database: `createdb -U admin -h localhost ml_automatization`
   - Or in pgAdmin 4: Create database `ml_automatization` with owner `admin` (password: `admin`).

5. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```

## Running
1. Activate virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Start the app:
   ```bash
   uvicorn main:app --reload
   ```

3. Open Swagger UI: `http://127.0.0.1:8000/docs`

## Testing
Use Swagger UI to test:
- **GET /tasks**: List all tasks.
- **POST /tasks**: Create a task (e.g., `{"title": "Test Task", "description": "Test", "completed": false}`).
- **PUT /tasks/{task_id}**: Update a task by UUID.
- **DELETE /tasks/{task_id}**: Delete a task by UUID.