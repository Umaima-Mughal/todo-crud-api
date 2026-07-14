from fastapi import FastAPI
from fastapi.responses import JSONResponse

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