import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.common.types import ExceptionResponse, SuccessResponse, CustomHTTPException, CustomORJSONResponse

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
    return CustomORJSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )



class I18nMiddleware(BaseHTTPMiddleware):
    WHITE_LIST = ['en', 'vn']

    async def dispatch(  # type: ignore
            self, request: Request, call_next: RequestResponseEndpoint):
        # 1. headers 2. path 3. query string
        locale = request.headers.get('locale', None) or \
                request.path_params.get('locale', None) or \
                request.query_params.get('locale', None) or \
                'en'

        if locale not in self.WHITE_LIST:
            locale = 'en'
        request.state.locale = locale

        return await call_next(request)