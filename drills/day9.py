from fastapi import FastAPI, HTTPException, status, Depends, APIRouter, Header
from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field

class JobApplicationCreate(BaseModel):
    company: str = Field(min_length=2, max_length=50)
    role: str = Field(min_length=2, max_length=50)
    salary: int | None = Field(default=None, gt=0)
    status: str = "Applied"

class JobApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    salary: int | None
    status: str
    created_at: str

APPLICATION_DB: list[dict[str, Any]] = []

def pagination_params(status:str | None=None, limit:int=10, skip:int=0) -> dict[str, Any]:
    limit = min(limit, 50)
    skip = max(skip, 0)
    return {"status": status, "limit": min(limit, 50), "skip": max(skip, 0)}


def verify_api_key(x_api_key: str = Header()) -> str:
    if x_api_key != "secret123":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: Invalid or missing X-API-Key")
    else:
        return x_api_key

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.get("/")
def list_applications(params: dict[str, Any] = Depends(pagination_params)) -> list[dict[str, Any]]:
    status_filter = params["status"]
    limit = params["limit"]
    skip = params["skip"]
    if status_filter is not None:
        results = [app for app in APPLICATION_DB if app["status"].lower() == status_filter.lower()]
        return results[skip: skip+limit]
    else:
        return APPLICATION_DB[skip: skip+limit]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobApplicationResponse)
def create_application(application: JobApplicationCreate) -> dict[str,Any]:
    id = len(APPLICATION_DB) + 1
    created_at = datetime.now().isoformat()
    records = {"id": id,
                **application.model_dump(),
                "created_at": created_at}
    APPLICATION_DB.append(records)
    return records

@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(app_id:int, api_key: str = Depends(verify_api_key)) -> None:
    for app in APPLICATION_DB:
        if app["id"] == app_id:
            APPLICATION_DB.remove(app)
            return None
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Application {app_id} not found")

app = FastAPI(title="Job Tracker Moduler API v3")
app.include_router(router)