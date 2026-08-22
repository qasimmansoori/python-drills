from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class ApplicationNotFoundError(Exception):
    def __init__(self, app_id: int):
        self.app_id = app_id


class DuplicateApplicationError(Exception):
    def __init__(self, company: str, role: str):
        self.company = company
        self.role = role


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationNotFoundError)
    async def application_not_found_handler(request: Request, exc: ApplicationNotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "error": {
                    "code": "APPLICATION_NOT_FOUND",
                    "message": f"Job application with ID {exc.app_id} was not found.",
                    "timestamp": datetime.now().isoformat(),
                },
            },
        )

    @app.exception_handler(DuplicateApplicationError)
    async def duplicate_application_handler(request: Request, exc: DuplicateApplicationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "error": {
                    "code": "DUPLICATE_APPLICATION",
                    "message": f"An application for {exc.role} at {exc.company} already exists.",
                    "timestamp": datetime.now().isoformat(),
                },
            },
        )
