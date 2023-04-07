from fastapi import FastAPI
from fastapi import status
from fastapi.exceptions import RequestValidationError, HTTPException

from app.database.db import session
from .configs.settings import ProjectSettings
from .routes.user import auth_router
from .utils.exception_handler import (
    custom_form_validation_error,
    http_exception_handler,
    unhandled_exception_handler
)
from .utils.middlewares import log_request_middleware

app = FastAPI(
    title=ProjectSettings.title,
    debug=ProjectSettings.debug,
    root_path_in_servers=ProjectSettings.root_path,
    openapi_url=f'{ProjectSettings.root_path}/openapi.json',
    docs_url=f'{ProjectSettings.root_path}/docs',
    redoc_url=f'{ProjectSettings.root_path}/redoc',
    version=ProjectSettings.version
)

app.mount(ProjectSettings.root_path, app)

app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, custom_form_validation_error)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.on_event("shutdown")
async def shutdown():
    await session.close()


@app.get("/ping", status_code=status.HTTP_200_OK)
async def health() -> str:
    return "pong"


app.include_router(auth_router)
