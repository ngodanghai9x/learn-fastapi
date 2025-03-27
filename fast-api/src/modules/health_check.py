from fastapi import FastAPI
from typing import Union
from fastapi.responses import FileResponse
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
    Security,
    Response
)
from starlette.responses import StreamingResponse
import io
from src.configs.env_setting import env
from src.common.types import ExceptionResponse, SuccessResponse, CustomHTTPException

router = APIRouter(
    # include_in_schema=True,
    prefix="/health",
    tags=["health"],
    # dependencies=[Depends(has_health_token)],
)

@router.get("/")
async def get_health():
    return SuccessResponse({
            "app_name": env.APP_NAME,
            "debug": env.DEBUG,
            # "secret": env.DB_PASSWORD.get_secret_value()
        })


# @router.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
