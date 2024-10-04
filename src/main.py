import uvicorn

from src.app import create_app
from src.config import parsed_config
from src.db.connection import setup_db

if __name__ == "__main__":
    setup_db()
    uvicorn.run(create_app(), host=parsed_config.API_HOST, port=parsed_config.API_PORT, reload=True)
