from logging import raiseExceptions

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import HTTPException, status
from starlette.responses import Response

app = FastAPI()
class TaskCreate(BaseModel):
    title: str


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):

    # Validation
    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    # Next ID
    next_id = tasks[-1]["id"] + 1

    # New task
    new_task = {
        "id": next_id,
        "title": task.title,
        "done": False
    }

    # Add to list
    tasks.append(new_task)

    # Return created task
    return new_task

app = FastAPI()

@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "ok"}

tasks = [{"id":1,"title":"Submit project report","done":True},
        {"id":2,"title":"Complete coding practice","done":False},
        {"id":3,"title":"Watch backend lecture","done":False}]

@app.get("/tasks")
def task():
    return tasks

@app.get("/tasks/{id}")
def get_task(id:int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )
# Stage 3: create with validation
class TaskCreate(BaseModel):
    title : str | None = None

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task(task : TaskCreate):
    if task.title is None or task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    else:
        next_id = tasks[-1]["id"] + 1
        new_task = {"id": next_id, "title":task.title, "done": False}
        tasks.append(new_task)
        return new_task

# Stage 4: full CRUD
class TaskUpdate(BaseModel):
    title : str | None = None
    done : bool | None = None

@app.put("/tasks/{id}")
def update_task(id:int,task:TaskUpdate):
    if task.title is None and task.done is None:
        raise HTTPException(
            status_code=400,
            detail="Empty/invalid body"
        )
    for t in tasks:
        if t["id"] == id:
            t["title"] = task.title
            t["done"] = task.done
            return t
    raise HTTPException(
                status_code=404,
                detail = "Unknown id"
            )

@app.delete("/tasks/{id}")
def delete(id:int):
    for t in tasks:
        if t["id"] == id:
            tasks.remove(t)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
                status_code=404,
                detail="Unknown id"
            )

