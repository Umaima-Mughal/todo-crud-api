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
