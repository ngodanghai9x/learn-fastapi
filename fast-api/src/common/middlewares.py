import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.common.types import ExceptionResponse, SuccessResponse, CustomHTTPException

# app = FastAPI()


# @app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    print('process_time', process_time)
    response.headers["X-Process-Time"] = str(process_time)
    return response

# @app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    formatted_errors = [
        {
            "field": ".".join(map(str, error["loc"])),  # body.email
            "message": error["msg"],
            "type": error["type"],
        }
        for error in errors
    ]

    raise CustomHTTPException(422, 'exception.422', {}, formatted_errors)
    # return JSONResponse(
    #     status_code=422,
    #     content={"errors": formatted_errors},  # Format chung cho toàn bộ app
    # )


async def http_exception_handler(request: Request, exc: CustomHTTPException):
    """Middleware bắt lỗi HTTPException và sửa lại format response"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )