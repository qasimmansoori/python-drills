from fastapi import FastAPI, status, HTTPException
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

app = FastAPI(title="Fastapi apis")

class JobApplicationCreate(BaseModel):
    company: str = Field(min_length=2, max_length=50)
    role: str = Field(min_length=2, max_length=50)
    salary: int | None = Field(default=None, gt=0)
    status: str = Field(default="Applied")

class JobApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    salary: int | None
    status: str
    created_at: str

APPLICATION_DB: list[dict[str, Any]] = []

@app.get("/")
def home():
    return {"status":"online", "version":"0.1.0"}

@app.post("/applications", status_code=status.HTTP_201_CREATED, response_model=JobApplicationResponse)
def create_application(application:JobApplicationCreate) -> dict[str,Any]:
    new_id = len(APPLICATION_DB)+1
    created_at = datetime.now().isoformat()
    records = {"id":new_id,
                **application.model_dump(),
                "created_at":created_at}
    APPLICATION_DB.append(records)

    return records

@app.get("/applications/{app_id}", response_model=JobApplicationResponse)
def get_job_result(app_id: int) -> dict[str,Any]:
    for app in APPLICATION_DB:
        if app["id"] == app_id:
            return app
    raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Application with id {app_id} not found"
    )

@app.get("/applications")
def list_applications(status: str | None = None, limit: int = 10) -> list[dict[str,Any]]:
    if status is None:
        return APPLICATION_DB[:limit]
    filtered = [app for app in APPLICATION_DB if app["status"].lower() == status.lower()]
    return filtered[:limit]