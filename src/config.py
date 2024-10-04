import os
from dotenv import load_dotenv
from pydantic import BaseModel, MongoDsn, Field

load_dotenv()

config = {
    'APP_NAME': os.getenv('APP_NAME'),
    'DB_NAME': os.getenv('DB_NAME'),
    'MONGO_URI': os.getenv('MONGO_URI') or '',
    'API_HOST': os.getenv('API_HOST'),
    'API_PORT': os.getenv('API_PORT')
}

class Config(BaseModel):
    APP_NAME: str
    DB_NAME: str
    MONGO_URI: MongoDsn
    API_HOST: str
    API_PORT: int = Field(gt=0, lt=65535)

def parse_config() -> Config:
    return Config(**config)

parsed_config = parse_config()
