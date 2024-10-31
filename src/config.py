import os
from dotenv import load_dotenv
from pydantic import Field, HttpUrl, MongoDsn, BaseModel

load_dotenv()

config = {
    'APP_NAME': os.getenv('APP_NAME'),
    'DB_NAME': os.getenv('DB_NAME'),
    'MONGO_URI': os.getenv('MONGO_URI') or '',
    'API_HOST': os.getenv('API_HOST'),
    'API_PORT': int(os.getenv('API_PORT') or '3000'),
    'CLALIT_BASE_URL': os.getenv('CLALIT_BASE_URL')
}

class Config(BaseModel):
    APP_NAME: str
    DB_NAME: str
    MONGO_URI: MongoDsn
    API_HOST: str
    API_PORT: int = Field(gt=0, lt=65535)
    CLALIT_BASE_URL: HttpUrl

def parse_config() -> Config:
    return Config(**config)

parsed_config = parse_config()
