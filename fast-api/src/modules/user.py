from fastapi import FastAPI
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

router = APIRouter(
    # include_in_schema=True,
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(has_user_token)],
)

@router.post(
    "/detect",
    response_model=dict,
    # status_code=status.HTTP_200_OK,
)
async def detect_in_image(
    # user_id: str = Form(..., description="Photo ID KYC"),
    # img_url: Optional[str] = Form(None, description="image url"),
    # image_s3_key: Optional[str] = Form(None, description="S3 key of the image"),
    # file: Optional[UploadFile] = File(None, description="Picture showing a face"),
):
    print()
    
    return {
        "abc": 1
        # "embedding": face_representation.embedding,
        # "image_s3_key": image_s3_key,
        # "face_detected": face_detected,
    }
