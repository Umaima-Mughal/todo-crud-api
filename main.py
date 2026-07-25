from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import HTTPException, status
from starlette.responses import Response
from contextlib import asynccontextmanager
from supabase_client import supabase

# DATABASE CONNECTION
from database import (
    create_table,
    seed_tasks,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
)

create_table()
seed_tasks()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server running and connected to Supabase")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/",summary="API information")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health",summary="Check API health")
def health():
    return {"status": "ok"}

tasks = [{"id":1,"title":"Submit project report","done":True},
        {"id":2,"title":"Complete coding practice","done":False},
        {"id":3,"title":"Watch backend lecture","done":False}]

initial_tasks = [
    {"id": 1, "title": "Submit project report", "done": True},
    {"id": 2, "title": "Complete coding practice", "done": False},
    {"id": 3, "title": "Watch backend lecture", "done": False},
]

@app.get("/tasks", summary="Get all tasks")
def task():
    return get_all_tasks()

@app.get("/tasks/{id}", summary="Get task by ID")
def get_task(id: int):
    task = get_task_by_id(id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return task

# Stage 3: create with validation
class TaskCreate(BaseModel):
    title : str | None = None

@app.post("/tasks",status_code=status.HTTP_201_CREATED, summary="Create a new task")
def add_task(task: TaskCreate):
    if task.title is None or task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    return create_task(task.title)

# Stage 4: full CRUD
class TaskUpdate(BaseModel):
    title : str | None = None
    done : bool | None = None

@app.put("/tasks/{id}", summary="Update a task")
def update_task_api(id: int, task: TaskUpdate):
    if task.title is None and task.done is None:
        raise HTTPException(
            status_code=400,
            detail="Empty/invalid body"
        )

    if task.title is not None and task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    updated = update_task(id, task.title, task.done)

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Unknown id"
        )

    return updated

@app.delete("/tasks/{id}", summary="Delete a task")
def delete_task_api(id: int):
    deleted = delete_task(id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Unknown id"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# reset
@app.post(
    "/reset",
    status_code=status.HTTP_200_OK,
    summary="Reset tasks to default",
)
def reset_tasks():
    global tasks

    tasks.clear()
    tasks.extend(task.copy() for task in initial_tasks)

    return {
        "message": "Tasks have been reset successfully.",
        "tasks": tasks
    }