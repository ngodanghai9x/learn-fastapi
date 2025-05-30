import uvicorn
import os
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.common.types import CustomORJSONResponse, CustomHTTPException
from src.common.middlewares import (
    add_process_time_header, 
    validation_exception_handler, 
    http_exception_handler,
    I18nMiddleware,
)
from src.configs.env_setting import env

from src.modules.user.routes import router as user_router
from src.modules.user.templates_routes import router as user_templates_router
from src.modules.health_check import router as health_check_router
from src.modules.sample import router as sample_router
from fastapi.exceptions import RequestValidationError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print(f'BASE_DIR {BASE_DIR}')

app = FastAPI(default_response_class=CustomORJSONResponse)

app.include_router(user_templates_router, tags=["user_templates"])
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(health_check_router, tags=["health"])
app.include_router(sample_router, tags=["sample_test"])

app.mount("/static", StaticFiles(directory="public"), name="public")

app.middleware("http")(add_process_time_header)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Hoặc cụ thể ["Authorization", "Content-Type"]
    expose_headers=["X-File-Status"],  # Thêm header cần expose ở đây
)
app.add_middleware(I18nMiddleware)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(CustomHTTPException, http_exception_handler)

@app.get("/")
async def main():
    return {"main": True}

if __name__ == "__main__":
    print(123)
    # uvicorn.run("src.main:app", host=env.APP_HOST, port=env.APP_PORT, reload=True)

print(f'Swagger running on http://{env.APP_HOST}:{env.APP_PORT}/docs')
