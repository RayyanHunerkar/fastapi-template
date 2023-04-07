import sys
from collections import defaultdict
from typing import Union

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response
from starlette import status

from .logger import logger


async def custom_form_validation_error(request, exc):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(str(filtered_loc))  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": "Invalid request", "errors": reformatted_message}
        ),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(request: Request, exc: Exception) -> PlainTextResponse:
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(
        f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value}>'
    )
    return PlainTextResponse(str(exc), status_code=500)
