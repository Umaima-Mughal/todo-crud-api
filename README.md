# Task API

A simple CRUD (Create, Read, Update and Delete) REST API built with **FastAPI**. This project was developed as part of a backend internship assignment to demonstrate REST API development, request validation, HTTP status codes, and automatic API documentation using Swagger UI.

---

## Features

- Create a new task
- Get all tasks
- Get a task by ID
- Update an existing task
- Delete a task
- Input validation
- Swagger UI documentation

---

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Run the API

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task |

---

## Example curl Output

```bash
curl -i http://127.0.0.1:8000/tasks
```

Example output:

```http
HTTP/1.1 200 OK
content-type: application/json

[
  {
    "id": 1,
    "title": "Submit project report",
    "done": true
  },
  {
    "id": 2,
    "title": "Complete coding practice",
    "done": false
  },
  {
    "id": 3,
    "title": "Watch backend lecture",
    "done": false
  }
]
```

---

## Swagger UI

FastAPI automatically generates interactive API documentation.

Open:

```
http://127.0.0.1:8000/docs
```
<img width="1897" height="873" alt="image" src="https://github.com/user-attachments/assets/25de8336-84d3-466f-be55-6ed4937b8bf8" />

## Example curl -i Output

```bash
curl -i http://127.0.0.1:8000/tasks
```
<img width="1791" height="331" alt="image" src="https://github.com/user-attachments/assets/f48fc1ac-9922-492b-98de-939507482d13" />

## PostgreSQL Database & Docker Setup

This version of the Task API uses PostgreSQL instead of SQLite.
The application follows a layered architecture where the database operations are isolated in the repository layer, allowing the storage engine to be changed without modifying API routes.

PostgreSQL runs inside a Docker container and data is persisted using a Docker volume.

---

## Run the Complete Stack

The complete application stack (FastAPI + PostgreSQL) can be started with one command:

```bash
docker compose up
```

---

## Environment Configuration

The application uses environment variables for database configuration.

Create a local `.env` file from the provided `.env.example`:

```bash
cp .env.example .env
```

Required environment variable:

```env
DATABASE_URL=postgresql://postgres:dev@db:5432/tasks
```

The database credentials are not hardcoded in the application.

- `.env` is ignored by Git.
- `.env.example` is committed to provide the required configuration format.

---

## Database Initialization

The PostgreSQL database is initialized automatically when the application starts.

The application:

- Creates the `tasks` table if it does not exist.
- Inserts three example tasks only on the first run.
- Preserves existing records across application and container restarts.

Database schema:

```sql
CREATE TABLE tasks(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
);
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task |

The API behaviour remains the same as the previous version, but the storage engine has been switched from SQLite to PostgreSQL.

---

## Example API Verification

Request:

```bash
curl -i http://127.0.0.1:8000/tasks
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
  },
  {
    "id": 2,
    "title": "Build CRUD API",
    "done": false
  },
  {
    "id": 3,
    "title": "Learn PostgreSQL",
    "done": false
  }
]
```

---

## Database Verification Screenshot

PostgreSQL database records were verified using the running database container.

Commands used:

```sql
\dt

SELECT * FROM tasks;
```

### PostgreSQL Database Screenshot

<img width="1472" height="639" alt="image" src="https://github.com/user-attachments/assets/4555376d-2156-4447-9abd-7ba0f89c47d0" />

---

## Persistence Verification

Persistence was tested by creating tasks and restarting the complete Docker stack.

Steps performed:

1. Created new tasks using the API.

2. Stopped the complete stack:

```bash
docker compose down
```

3. Started the stack again:

```bash
docker compose up
```

4. Verified that previously created tasks were still available.

The data remained available because PostgreSQL uses a Docker volume for persistent storage.

---

## Docker Compose Architecture

The complete stack consists of two services:

| Service | Purpose |
|---------|---------|
| api | FastAPI application |
| db | PostgreSQL database |

The API connects to PostgreSQL using the Docker service name:

```
db
```

instead of:

```
localhost
```

This allows the complete application stack to run with a single command:

```bash
docker compose up
```

---

## Clean Clone Verification

A new user can run the project without manual database setup.

Steps:

```bash
git clone <repository-url>

cd todo-crud-api

cp .env.example .env

docker compose up
```

After startup, the API works and seeded tasks can be retrieved:

```bash
curl http://127.0.0.1:8000/tasks
```
