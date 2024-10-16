from fastapi import APIRouter

basic_router = APIRouter(prefix='')

@basic_router.get('/health')
def get_health() -> str:
    return "I am alive and kicking"
