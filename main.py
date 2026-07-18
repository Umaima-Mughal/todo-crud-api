from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import HTTPException, status
from starlette.responses import Response

app = FastAPI()

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
    return tasks

@app.get("/tasks/{id}",summary="Get task by ID")
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

@app.post("/tasks",status_code=status.HTTP_201_CREATED, summary="Create a new task")
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

@app.put("/tasks/{id}", summary="Update a task")
def update_task(id:int,task:TaskUpdate):
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
    for t in tasks:
        if t["id"] == id:
            if task.title is not None:
                t["title"] = task.title

            if task.done is not None:
                t["done"] = task.done
            return t
    raise HTTPException(
                status_code=404,
                detail = "Unknown id"
            )

@app.delete("/tasks/{id}", summary="Delete a task")
def delete(id:int):
    for t in tasks:
        if t["id"] == id:
            tasks.remove(t)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
                status_code=404,
                detail="Unknown id"
            )

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