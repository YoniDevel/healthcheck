import uvicorn

from src.app import app
from src.config import parsed_config

if __name__ == "__main__":
    uvicorn.run("main:app", host=parsed_config.API_HOST, port=parsed_config.API_PORT, reload=True)
