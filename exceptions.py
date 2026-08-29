from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class CustomAPIException(HTTPException):
    def __init__(self, status_code: int, error: str, message: str):
        super().__init__(
            status_code=status_code,
            detail={"error": error, "message": message},
        )


def _serializable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {_serializable(k): _serializable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_serializable(v) for v in value]
    return str(value)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(CustomAPIException)
    async def custom_api_exception_handler(
        request: Request, exc: CustomAPIException
    ) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "message": [_serializable(error) for error in exc.errors()],
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Server Error", "message": "Unexpected error occurred"},
        )
