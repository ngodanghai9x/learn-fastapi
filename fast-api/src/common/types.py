from typing import Optional, Dict, Any, Literal, Union
from pprint import pprint
from fastapi import FastAPI, Response, HTTPException
import orjson

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, message_code: str = 'exception.common', message_code_args: Dict[str, Any] = {}, data: Dict[str, Any] = {},  headers: dict[str, str] | None = None):
        self.detail = 'CustomHTTPException'
        self.status_code = status_code
        self.message_code = message_code
        self.message_code_args = message_code_args or {}
        self.data = data or {}

        super().__init__(status_code=status_code, detail={
            "status_code": self.status_code,
            "message_code": self.message_code,
            "message_code_args": self.message_code_args,
            "data": self.data,
        }, headers=headers)

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "message_code": self.message_code,
            "message_code_args": self.message_code_args,
            "data": self.data,
        }

class SuccessResponse:
    def __init__(self, data: Dict[str, Any], message_code: str = 'success.common'):
        self.data = data
        self.message_code = message_code
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {"data": self.data, "message_code": self.message_code}

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()

    # def to_json(self) -> str:
    #     return json.dumps({"data": self.data, "message_code": self.message_code})

class ExceptionResponse:
    def __init__(self, message_code: str = 'exception.common', message_code_args: Dict[str, Any] = {}, data: Dict[str, Any] = {}):
        self.data = data
        self.message_code = message_code
        self.message_code_args = message_code_args
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "message_code": self.message_code,
            "message_code_args": self.message_code_args
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()

    # def to_json(self) -> str:
    #     return json.dumps({
    #         "data": self.data,
    #         "message_code": self.message_code,
    #         "message_code_args": self.message_code_args
    #     })

class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"

        # if isinstance(content, ErrorResp):
        #     print('isinstance')
        #     pprint(content)
        #     content = content.to_dict() 
        
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)