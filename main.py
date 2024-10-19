import uvicorn

from src import parsed_config

if __name__ == "__main__":
    uvicorn.run('src:app', host=parsed_config.API_HOST, port=parsed_config.API_PORT, reload=True)
