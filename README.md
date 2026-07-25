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

# Supabase Authentication

This stage adds authentication and authorization using **Supabase Auth**.

Supabase is used as an external authentication provider to manage users and generate JWT access tokens.

Implemented features:

- User signup
- User login
- JWT access token generation
- Protected routes
- Token verification
- Logout functionality
- Swagger UI Bearer authentication

---

# Environment Variables

Authentication credentials are stored using environment variables.

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

Important:

- `.env` is added to `.gitignore`.
- Supabase keys and secrets are never committed to GitHub.
- `.env.example` is provided as a template.

---

# Authentication Flow

## Signup

Create a new user account:

```
POST /auth/signup
```

Example request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:

```
201 Created
```

---

## Login

Authenticate a user and receive access tokens:

```
POST /auth/login
```

Example request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "JWT_ACCESS_TOKEN",
  "refresh_token": "JWT_REFRESH_TOKEN"
}
```

The access token is required to access protected routes.

---

# Protected Routes

Protected routes require a valid Bearer token:

```
Authorization: Bearer <access_token>
```

The API verifies the token using Supabase before allowing access.

Invalid, expired, or missing tokens return:

```json
{
  "detail": "Invalid or expired token"
}
```

with:

```
401 Unauthorized
```

---

# Logout

Logout is implemented as a protected endpoint:

```
POST /auth/logout
```

The endpoint verifies the user's token and signs out the session using Supabase.

Successful logout returns:

```
204 No Content
```

---

# API Reference

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/auth/signup` | Create user account | No |
| POST | `/auth/login` | Login and receive access token | No |
| POST | `/auth/logout` | Logout current user | Yes |
| GET | `/public/info` | Public information endpoint | No |
| GET | `/protected/profile` | Get authenticated user profile | Yes |
| GET | `/protected/dashboard` | Protected dashboard endpoint | Yes |

---

# Swagger UI Authentication

FastAPI automatically generates interactive API documentation:

```
http://127.0.0.1:8000/docs
```

Swagger UI provides an **Authorize 🔒 button** for protected routes.

Steps:

1. Login using `/auth/login`.
2. Copy the returned `access_token`.
3. Click the **Authorize** button.
4. Enter:

```
Bearer <access_token>
```

5. Execute protected endpoints directly from Swagger UI.

Protected endpoints will only be accessible with a valid token.

---

# Swagger UI Screenshot

The screenshot below shows Swagger UI with protected routes and Bearer authentication enabled.

<img width="1476" height="707" alt="image" src="https://github.com/user-attachments/assets/e7d01978-901e-4a02-96ab-424007ce7467" />
