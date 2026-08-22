from fastapi import APIRouter
from projects.job_tracker.app.api.v1.endpoints.applications import router as applications_router

api_router = APIRouter()
api_router.include_router(applications_router)
