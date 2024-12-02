
import boto3
from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse, Response
from botocore.exceptions import NoCredentialsError
from typing import Optional
import config  # Giả sử bạn có một file config chứa thông tin của AWS

router = APIRouter()

@router.get("/kyc/img-kycs/{img_kyc_id}/images/{image_type}")
async def get_img_kyc_image(img_kyc_id: int, image_type: str):
    # Xây dựng URL ảnh trên S3
    s3_base_url = "https://your_s3_base_url"
    image_url = f"{s3_base_url}/{img_kyc_id}/{image_type}.jpg"
    
    # Trả về mã redirect 302
    return Response(status_code=302, headers={"Location": image_url})



router = APIRouter()

# Khởi tạo s3 client (dùng hàm get_s3_client trong trường hợp cần tái sử dụng)
def get_s3_client():
    return boto3.client(
        service_name='s3',
        aws_access_key_id=config.AMAZON_S3_ACCESS_KEY,
        aws_secret_access_key=config.AMAZON_S3_SECRET_KEY.get_secret_value(),
        region_name=config.AMAZON_S3_REGION  # Hoặc bỏ nếu không cần region
    )

# API endpoint trả về URL ký
@router.get("/kyc/img-kycs/{img_kyc_id}/images/{image_type}")
async def get_img_kyc_image(img_kyc_id: int, image_type: str):
    # S3 bucket và key của ảnh
    s3_bucket = config.AMAZON_S3_BUCKET
    s3_key = f"{img_kyc_id}/{image_type}.jpg"  # Key ảnh có thể được thay đổi tùy thuộc vào cấu trúc của bạn
    
    s3_client = get_s3_client()

    try:
        # Generate signed URL từ S3
        url = s3_client.generate_presigned_url('get_object', 
                                                Params={'Bucket': s3_bucket, 'Key': s3_key},
                                                ExpiresIn=3600)  # URL có hiệu lực trong 1 giờ (3600 giây)
        # Trả về redirect tới URL ký
        return RedirectResponse(url=url)

    except NoCredentialsError:
        return {"error": "AWS credentials not found."}  # Xử lý nếu không tìm thấy credentials
    except Exception as e:
        return {"error": str(e)}  # Xử lý các lỗi khác

