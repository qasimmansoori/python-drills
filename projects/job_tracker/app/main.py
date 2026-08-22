from fastapi import FastAPI

from projects.job_tracker.app.api.v1.router import api_router
from projects.job_tracker.app.core.exceptions import register_exception_handlers
from projects.job_tracker.app.core.middleware import register_middleware


def create_application() -> FastAPI:
    app = FastAPI(
        title="Job Application Tracker API",
        description="Production modular FastAPI backend for managing tech job applications.",
        version="1.0.0",
    )

    # 1. Register Global Middleware
    register_middleware(app)

    # 2. Register Global Custom Exception Handlers
    register_exception_handlers(app)

    # 3. Mount API v1 Routes
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health", tags=["Health"])
    def health_check() -> dict[str, str]:
        return {"status": "healthy", "service": "job-tracker-api"}

    return app


app = create_application()
