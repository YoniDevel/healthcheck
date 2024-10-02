import os
from dotenv import load_dotenv
from pydantic import BaseModel, MongoDsn

load_dotenv()

config = {
    'DB_NAME': os.getenv('DB_NAME'),
    'MONGO_URI': os.getenv('MONGO_URI') or '',
}

class Config(BaseModel):
    DB_NAME: str
    MONGO_URI: MongoDsn

def parse_config() -> Config:
    return Config(**config)

parsed_config = parse_config()
