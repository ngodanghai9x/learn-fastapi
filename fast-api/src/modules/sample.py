import io
import os
import shutil
from fastapi import FastAPI
from typing import Union, Annotated
from fastapi.responses import FileResponse
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    BackgroundTasks,
    Query,
    UploadFile,
    status,
    Security,
    Body,
    Cookie,
    Response,
    Request
)
from src.configs.env_setting import env
from src.common.translator import Translator
from src.common.types import ExceptionResponse, SuccessResponse, CustomHTTPException
from src.common.utils import file_iterator, afile_iterator, to_safe_filename
from src.entities import get_async_db, async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse
from datetime import datetime, time, timedelta
from pprint import pprint

UPLOAD_DIR = 'uploads' or env.UPLOAD_DIR

router = APIRouter(
    # include_in_schema=True,
    prefix="/sample/test",
    # dependencies=[Depends(has_health_token)],
)

async def slow_func(name: str):
    print(f'slow func {name} is running ')
    async with await async_session_maker() as db:
        pprint(db)
    pass

@router.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

@router.put("/items/{item_id}")
async def read_items(
    item_id: str,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }


@router.post("/save")
async def save_file(
    img: Annotated[UploadFile, File()],
    background_tasks: BackgroundTasks,  # = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    # image_bytes = await img.read()

    file_uuid = 'uuid.uuid4()'
    # safe_filename = to_safe_filename(f'{datetime.utcnow().timestamp()}{cutted_image.filename}')
    safe_filename = to_safe_filename(f'{img.filename}')

    saved_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(img.file, buffer)  # Sao chép nội dung file vào local

    background_tasks.add_task(slow_func, '1st')
    background_tasks.add_task(slow_func, '2nd')

    return SuccessResponse({
            "saved_path": saved_path,
            "safe_filename": safe_filename,
        })

@router.get("/download")
async def download_file():
    # Giả sử đây là dữ liệu file được tạo động
    file_content = b"Hello, this is a file content in bytes."

    # Chuyển bytes thành một stream (io.BytesIO)
    file_stream = io.BytesIO(file_content)
    file_stream = afile_iterator( os.path.join(UPLOAD_DIR, 'abc.txt'))

    # Trả về file với dạng StreamingResponse
    return StreamingResponse(
        file_stream, 
        media_type="application/octet-stream", 
        headers={"Content-Disposition": "inline"}
        # headers={"Content-Disposition": "attachment; filename=example.txt"}
    )

@router.get('/my-resource')
def get_my_resource(request: Request): 
    translator = Translator(request.state.locale)
    # 'hello world'
    print(translator.t('exception.hello'))
    # 'Hi, Jon Doe'
    # print(translator.t('exception.common'), user_name='Jon Doe')

    return SuccessResponse({
            "mes": translator.t('exception.common', user_name='Jon Doe'),
            "hi" : translator.t('exception.hello')
        })

@router.get("/resp")
async def read_root():

    raise CustomHTTPException(400, 'exception.common', {
        "app_name": env.APP_NAME,
        "debug": env.DEBUG,
        # "secret": env.DB_PASSWORD.get_secret_value()
    })

    raise HTTPException(status_code=400, detail=ExceptionResponse('error.required',{
        "app_name": env.APP_NAME,
        "debug": env.DEBUG,
        # "secret": env.DB_PASSWORD.get_secret_value()
    }).to_dict())

    raise HTTPException(status_code=400, detail={
            "app_name": env.APP_NAME,
            "debug": env.DEBUG,
            # "secret": env.DB_PASSWORD.get_secret_value()
        })

    return FileResponse('./abcx.txt')

    return SuccessResponse({
            "app_name": env.APP_NAME,
            "debug": env.DEBUG,
            # "secret": env.DB_PASSWORD.get_secret_value()
        })


# @router.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
