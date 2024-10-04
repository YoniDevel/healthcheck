from fastapi import FastAPI

from src.routes.basic import basic_router

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(basic_router)
    return app
