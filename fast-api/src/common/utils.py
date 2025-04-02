# import httpx
from typing import Optional, Dict, Any, Literal, Union, AsyncGenerator
import re
import aiofiles
import asyncio

async def async_file_iterator(file_path: str) -> AsyncGenerator[bytes, None]:
    try:
        if not file_path:
            return  # Không cần `return None`, chỉ cần `return` là đủ

        await asyncio.sleep(0.1)  # Cho hệ điều hành có thời gian ghi xong

        async with aiofiles.open(file_path, mode="rb") as f:
            while chunk := await f.read(1024):  # Đọc từng chunk 1024 bytes
                yield chunk

    except Exception as e:
        print(f"Error reading file: {e}")
        return 

def file_iterator(file_path: str):
    with open(file_path, mode="rb") as f:
        yield from f

def to_safe_filename(filename: str) -> str:
    safe_filename = re.sub(r"[^\w.-]", "_", filename)

    return safe_filename

# # Hàm gọi API chung với method và URL tùy chỉnh
# async def call_api(
#     method: Literal['GET', 'POST', 'PUT', 'DELETE'], 
#     url: str, 
#     params: Optional[Dict[str, Any]] = None, 
#     headers: Optional[Dict[str, str]] = None, 
#     json: Optional[Dict[str, Any]] = None,
#     data: Optional[Dict[str, Union[str, int, float]]] = None,
#     files: Optional[Dict[str, Any]] = None
# ) -> httpx.Response:
#     """
#     Hàm gọi API chung với các method khác nhau: GET, POST, PUT, DELETE.
    
#     :param method: Method HTTP (GET, POST, PUT, DELETE)
#     :param url: URL của API cần gọi
#     :param params: Tham số URL (tùy chọn)
#     :param headers: Thông tin header (tùy chọn)
#     :param json: Dữ liệu JSON cho body (tùy chọn)
#     :param data: Dữ liệu form-data cho body (tùy chọn)
#     :param files: File gửi qua form-data (tùy chọn)
    
#     :return: Kết quả trả về từ API dưới dạng dict
#     """
#     async with httpx.AsyncClient() as client:
#         response = await client.request(
#             method, 
#             url, 
#             params=params, 
#             headers=headers, 
#             json=json,
#             data=data,
#             files=files
#         )
#         # Kiểm tra nếu status code không phải 200
#         response.raise_for_status()
#         return response  # Trả về kết quả dưới dạng dict

# # Hàm gọi API POST với body là JSON và API Key trên header
# async def call_api_post_with_json(
#     url: str, 
#     json_body: Dict[str, Any], 
#     api_key: str
# ) -> dict:
#     """
#     Hàm gọi API POST với body là JSON và API Key được thêm vào header.
    
#     :param url: URL của API cần gọi
#     :param json_body: Dữ liệu JSON cần gửi trong body của POST request
#     :param api_key: API Key cần gửi trong header
    
#     :return: Kết quả trả về từ API dưới dạng dict
#     """
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json; charset=UTF-8",
#     }
    
#     # Gọi API POST thông qua hàm call_api
#     resp = await call_api(
#         method="POST",
#         url=url,
#         headers=headers,
#         json=json_body
#     )

#     return resp.json()

# # Hàm gọi API POST với form-data và file
# async def call_api_post_with_form_and_file(
#     url: str, 
#     form_data: Dict[str, Union[str, int, float]], 
#     file_path: str, 
#     file_key: str = "file",
#     api_key: Optional[str] = None
# ) -> dict:
#     """
#     Hàm gọi API POST với form-data và gửi kèm file.

#     :param url: URL của API cần gọi
#     :param form_data: Dữ liệu form-data cần gửi
#     :param file_path: Đường dẫn file cần gửi
#     :param file_key: Tên key của file trong form-data (default: "file")
#     :param api_key: API Key (nếu cần thêm vào header)
    
#     :return: Kết quả trả về từ API dưới dạng dict
#     """
#     headers = {
#         "Content-Type": "multipart/form-data",
#     }
#     if api_key:
#         headers["Authorization"] = f"Bearer {api_key}"

#     # Đọc file và tạo object file để gửi
#     with open(file_path, "rb") as file:
#         files = {file_key: (file_path, file, "application/octet-stream")}
        
#         # Gọi API với form-data và file
#         return await call_api(
#             method="POST",
#             url=url,
#             headers=headers,
#             data=form_data,
#             files=files
#         )
    
# # Hàm gọi API POST với form-data và stream file từ URL
# async def call_api_post_with_form_and_stream(
#     url: str, 
#     form_data: Dict[str, Union[str, int, float]], 
#     file_stream_url: str, 
#     file_key: str = "file",
#     api_key: Optional[str] = None
# ) -> dict:
#     """
#     Hàm gọi API POST với form-data và gửi file stream từ một URL.

#     :param url: URL của API cần gọi
#     :param form_data: Dữ liệu form-data cần gửi
#     :param file_stream_url: URL của file cần tải và gửi
#     :param file_key: Tên key của file trong form-data (default: "file")
#     :param api_key: API Key (nếu cần thêm vào header)
    
#     :return: Kết quả trả về từ API dưới dạng dict
#     """
#     headers = {
#         "Content-Type": "multipart/form-data",
#     }
#     if api_key:
#         headers["Authorization"] = f"Bearer {api_key}"

#     async with httpx.AsyncClient() as client:
#         # Tải file stream từ URL
#         async with client.stream("GET", file_stream_url) as file_response:
#             file_response.raise_for_status()

#             # Đọc file stream để gửi
#             files = {
#                 file_key: (file_stream_url.split("/")[-1], file_response.aiter_bytes(), "application/octet-stream")
#             }

#             # Gửi form-data và stream file đến API
#             response = await client.request(
#                 method="POST",
#                 url=url,
#                 headers=headers,
#                 data=form_data,
#                 files=files
#             )
#             response.raise_for_status()
#             return response.json()

# async def main():
#     try:
#         api_url = "https://jsonplaceholder.typicode.com/posts"
#         api_key = "your-api-key"
        
#         # ========= Gọi API POST với JSON body ========= 
#         json_data = {
#             'title': 'foo',
#             'body': 'bar',
#             'userId': 2,
#         }

#         resp1 = await call_api('GET', api_url, params={'userId': 3})
#         print("🐍 File: httpx/callApi.py | Line: 80 | undefined ~ resp1",resp1)
        
#         resp2 = await call_api_post_with_json(api_url, json_data, api_key)
#         print("🐍 File: httpx/callApi.py | Line: 77 | undefined ~ resp2",resp2)


#         # ========= Gọi API POST với form-data và stream file từ URL ========= 
#         form_data = {
#             'userId': 123,
#             'description': 'This is a test upload',
#         }

#         # Đường dẫn file
#         file_path = "example.txt"        
#         # URL file cần stream
#         file_stream_url = "https://via.placeholder.com/150"

#         # Gọi API POST với form-data và file
#         resp3 = await call_api_post_with_form_and_file(api_url, form_data, file_path, api_key=api_key)
#         print("Response from API with form-data and file:", resp3)

#         # Gọi API POST với form-data và file stream
#         resp4 = await call_api_post_with_form_and_stream(api_url, form_data, file_stream_url, api_key=api_key)
#         print("Response from API with form-data and streamed file:", resp4)
        
#     except Exception as e:
#         print(e)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
