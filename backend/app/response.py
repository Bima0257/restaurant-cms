from typing import Any

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    success: bool = False
    message: str = ""
    errors: Any = None


def success_response(data: Any = None, message: str = "Success") -> dict:
    return {"success": True, "message": message, "data": data}


def http_exception_handler(request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.detail,
        ).model_dump(),
    )


def validation_exception_handler(request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for err in exc.errors():
        field = ".".join(str(l) for l in err.get("loc", []))
        msg = err.get("msg", "Invalid value")
        if field and field != "body":
            errors.append({"field": field, "message": msg})
        else:
            errors.append({"field": "body", "message": msg})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            message="Validation failed",
            errors=errors,
        ).model_dump(),
    )


def generic_exception_handler(request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            message="An internal server error occurred",
        ).model_dump(),
    )
