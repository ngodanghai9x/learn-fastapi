from fastapi import FastAPI
from typing import Union
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
)
from configs.env_setting import env

router = APIRouter(
    # include_in_schema=True,
    prefix="/health",
    tags=["health"],
    # dependencies=[Depends(has_health_token)],
)


@router.get("/")
async def read_root():
    return {
            "app_name": env.app_name,
            "debug": env.debug,
            "secret_key": env.secret_key.get_secret_value()
        }


@router.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
