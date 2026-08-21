from fastapi import FastAPI, Depends, Request, status, Header, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
import time
from typing import Any

app = FastAPI(title="API Exceptional handler")

class ApplicationNotFoundError(Exception):
    def __init__(self, app_id: int):
        self.app_id = app_id

class DuplicateApplicationError(Exception):
    def __init__(self, company: str, role: str):
        self.company = company
        self.role = role

APPLICATION_DB: list[dict[str, Any]] = []

class JobApplicationCreate(BaseModel):
    company: str = Field(min_length=2, max_length=50)
    role: str = Field(min_length=2, max_length=50)
    salary: int | None = Field(default=None)
    status: str = Field(default="Applied")

class JobApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    salary: int | None = None
    status: str 
    created_at: str

@app.exception_handler(ApplicationNotFoundError)
async def app_not_found_handler(request: Request, exc: ApplicationNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "success": False,
            "error": {
                "code": "Application not found",
                "message": f"Application with id: {exc.app_id} was not found",
                "timestamp": datetime.now().isoformat(),
            },
        },
    )

@app.exception_handler(DuplicateApplicationError)
async def duplicate_app_handler(request: Request, exc: DuplicateApplicationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error":{
                "success":False,
                "message": f"Application for {exc.role} at {exc.company} already exists",
                "timestamp": datetime.now().isoformat()
            },
        },
    )

@app.middleware("http")
async def add_process_time_handler(request:Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["x-process-Time"] = f"{process_time:.5f}s"
    return response

router = APIRouter(prefix="/application", tags=["Applications"])

