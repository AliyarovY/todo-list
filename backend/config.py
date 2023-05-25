import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    secret_key: str = 'super secret string'  # Change this!
    debug: bool = False

    server_host: str = '127.0.0.1'
    server_port: int = 5000

    database_url: str


settings = Settings(
    _env_file=os.path.join(BASE_DIR, '.env'),
    _env_file_encoding='utf-8',
)
