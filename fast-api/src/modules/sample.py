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
    Query,
    UploadFile,
    status,
    Security,
    Response
)
from src.configs.env_setting import env
from src.common.types import ExceptionResponse, SuccessResponse, CustomHTTPException
from src.common.utils import file_iterator, afile_iterator, to_safe_filename
from src.entities import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

UPLOAD_DIR = '/home/gem/Documents/MyRepo/learn-fastapi/fast-api/uploads' or env.UPLOAD_DIR

router = APIRouter(
    # include_in_schema=True,
    prefix="/sample/test",
    # dependencies=[Depends(has_health_token)],
)
@router.post("/save")
async def save_file(
    img: Annotated[UploadFile, File()],
    db: AsyncSession = Depends(get_async_db),
):
    # image_bytes = await img.read()

    file_uuid = 'uuid.uuid4()'
    # safe_filename = to_safe_filename(f'{datetime.utcnow().timestamp()}{cutted_image.filename}')
    safe_filename = to_safe_filename(f'{img.filename}')

    saved_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(img.file, buffer)  # Sao chép nội dung file vào local

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
