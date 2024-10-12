from fastapi import FastAPI

from src.routes.basic import basic_router
from src.routes.users import users_router

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(basic_router)
    app.include_router(users_router)
    return app
