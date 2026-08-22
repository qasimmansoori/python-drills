from datetime import datetime
from typing import Any
from fastapi import APIRouter, Depends, Header, HTTPException, status

from projects.job_tracker.app.core.exceptions import (
    ApplicationNotFoundError,
    DuplicateApplicationError,
)
from projects.job_tracker.app.schemas.application import (
    JobApplicationCreate,
    JobApplicationResponse,
)

router = APIRouter(prefix="/applications", tags=["Job Applications"])

# In-memory storage for Phase 1
APPLICATIONS_STORE: list[dict[str, Any]] = []


def get_pagination_params(
    status: str | None = None,
    limit: int = 10,
    skip: int = 0,
) -> dict[str, Any]:
    return {
        "status": status,
        "limit": min(max(limit, 1), 50),
        "skip": max(skip, 0),
    }


def verify_admin_key(x_api_key: str = Header(..., description="Admin API secret header")) -> str:
    if x_api_key != "secret123":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing X-API-Key header",
        )
    return x_api_key


@router.get("/", response_model=list[JobApplicationResponse])
def list_applications(
    params: dict[str, Any] = Depends(get_pagination_params),
) -> list[dict[str, Any]]:
    status_filter = params["status"]
    limit = params["limit"]
    skip = params["skip"]

    if status_filter:
        filtered = [
            app for app in APPLICATIONS_STORE
            if app["status"].lower() == status_filter.lower()
        ]
    else:
        filtered = APPLICATIONS_STORE

    return filtered[skip : skip + limit]


@router.post("/", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application_in: JobApplicationCreate) -> dict[str, Any]:
    # Check for duplicate
    for existing in APPLICATIONS_STORE:
        if (
            existing["company"].lower() == application_in.company.lower()
            and existing["role"].lower() == application_in.role.lower()
        ):
            raise DuplicateApplicationError(application_in.company, application_in.role)

    new_id = len(APPLICATIONS_STORE) + 1
    new_record = {
        "id": new_id,
        **application_in.model_dump(),
        "created_at": datetime.now().isoformat(),
    }
    APPLICATIONS_STORE.append(new_record)
    return new_record


@router.get("/{app_id}", response_model=JobApplicationResponse)
def get_application(app_id: int) -> dict[str, Any]:
    for app in APPLICATIONS_STORE:
        if app["id"] == app_id:
            return app
    raise ApplicationNotFoundError(app_id)


@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    app_id: int,
    _auth: str = Depends(verify_admin_key),
) -> None:
    for app in APPLICATIONS_STORE:
        if app["id"] == app_id:
            APPLICATIONS_STORE.remove(app)
            return None
    raise ApplicationNotFoundError(app_id)
