from typing import Any, AsyncGenerator
from pymongo.errors import PyMongoError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException, Request, status

from src.config import parsed_config
from src.routes.basic import basic_router
from src.routes.users import users_router
from src.db.connection import disconnect_mongo, connect_mongo

def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
        connect_mongo()
        yield
        disconnect_mongo()
    
    app = FastAPI(lifespan=lifespan, title=parsed_config.APP_NAME)
    app.include_router(basic_router)
    app.include_router(users_router)
    
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": exc.errors(),
            "body": exc.body
        }
    )
        
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.detail
            }
        )

    @app.exception_handler(PyMongoError)
    async def mongo_error_exception_handler(_: Request, exc: PyMongoError) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"unexpected mongo db error: {exc._message}"                
            }
        )

    return app

app = create_app()
