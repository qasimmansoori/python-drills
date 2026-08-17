from fastapi import FastAPI, status
from typing import Any
from pydantic import BaseModel


class JobApplicationCreate(BaseModel):
    company: str
    role: str
    salary: int | None = None
    status: str = "Applied"

APPLICATION_DB: list[dict[str, Any]] = []

app = FastAPI(title="Job tracker API", version="0.1.0")

@app.get("/")
def get_home() -> dict:
    return {"status":"online","version":"0.1.0"}

@app.get("/application/{app_id}")
def get_application_status(app_id: int)->dict:
    return {"application_id": app_id, "company": "Acme Corp", "status": "Applied"}

@app.get("/applications")
def list_applications(status: str | None = None, limit: int = 10) -> dict[str, Any]:
    if status is None:
        return {"filter_status": "all",
        "limit": limit,
        "results": APPLICATION_DB[:limit]}

    else:
        filtered = [app for app in APPLICATION_DB if app["status"].lower() == status.lower()]
        return {"filter_status": status, "limit": limit, "results": filtered[:limit]}


@app.post("/applications", status_code=status.HTTP_201_CREATED) 
def create_application(application: JobApplicationCreate, ) -> dict[str, Any]:
    id = len(APPLICATION_DB) + 1
    record = {"id": id,
              **application.model_dump()}
    APPLICATION_DB.append(record)
    return record

@app.delete("/applications/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(app_id: int) -> None:
    for app in APPLICATION_DB:
        if app["id"] == app_id:
            APPLICATION_DB.remove(app)
            return None
    return None
