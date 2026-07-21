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

---

# Database (SQLite)

## Why SQLite was chosen

SQLite was chosen because it requires zero setup and stores the complete database in a single file.

It is lightweight, easy to integrate, and allows data to persist between application restarts without requiring a separate database server.

For this project, SQLite provides a simple and reliable way to demonstrate CRUD operations with real database persistence.

---

## Database Location

The SQLite database file is stored in the project root directory:

```text
tasks.db
```

The database file is created automatically when the application starts.

It is usually git-ignored, so each fresh clone starts with a new database that is automatically created with the required table and initial data.

---

## Automatic Database Creation

No manual database setup is required.

After installing dependencies, running:

```bash
uvicorn main:app --reload
```

automatically:

- Creates the `tasks.db` SQLite database
- Creates the `tasks` table
- Inserts the initial seeded tasks

This allows anyone cloning the repository to run the project without additional database configuration.

---

## Example SQL Query Executed

The following query was executed in **DB Browser for SQLite** during Stage 4:

```sql
SELECT * FROM tasks;
```

This query retrieves all tasks stored in the database.


## Database Viewer Screenshot

The SQLite database was inspected using **DB Browser for SQLite**.

The screenshot below shows the `tasks` table and stored records:

<img width="975" height="513" alt="Database Screenshot" src="https://github.com/user-attachments/assets/c17d3d59-a29e-4e89-afca-557af2883162" />

---
