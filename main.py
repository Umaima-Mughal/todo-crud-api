from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import Response
from contextlib import asynccontextmanager
from supabase_client import supabase

# DATABASE CONNECTION
from database import (
    create_table,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    print("Server running and connected")
    yield

app = FastAPI(lifespan=lifespan)

security = HTTPBearer()

# SUPABASE AUTH IMPLEMENTATION
class AuthRequest(BaseModel):
    email: str
    password: str

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)

        return {
            "user": response.user,
            "token": token
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


@app.post("/auth/signup", status_code=201)
def signup(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up(
            {
                "email": data.email,
                "password": data.password
            }
        )
        return response.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login")
def login(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": data.email,
                "password": data.password
            }
        )

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }

@app.get("/protected/profile")
def protected_profile(current_user = Depends(get_current_user)):

    user = current_user["user"]

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }

@app.get("/protected/dashboard")
def dashboard(current_user = Depends(get_current_user)):
    return {
        "message": "Welcome to dashboard"
    }

@app.post("/auth/logout", status_code=204)
def logout(current_user = Depends(get_current_user)):

    supabase.auth.sign_out(
        current_user["token"]
    )

    return Response(status_code=204)


@app.get("/",summary="API information")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health",summary="Check API health")
def health():
    return {"status": "ok"}

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

