
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI

class CustomAPIException(HTTPException):
    def __init__(self, status_code: int, error: str, message: str):
        super().__init__(
            status_code=status_code,
            detail={"error": error, "message": message},
        )

def register_exception_handlers(app: FastAPI):
    
    @app.exception_handler(CustomAPIException)
    async def custom_api_exception_handler(request: Request, exc: CustomAPIException):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "Validation Error", "message": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Server Error", "message": "Unexpected error occurred"},
        )
