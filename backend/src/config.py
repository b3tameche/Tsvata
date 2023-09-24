import configparser

from sqlalchemy import URL, text
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

config = configparser.ConfigParser()
config.read(ROOT_DIR / 'config.ini')

class Config:

    DB_URL = URL.create(
        drivername = config.get('database', 'DB_DRIVER'),
        username = config.get('database', 'DB_USERNAME'),
        password = config.get('database', 'DB_PASSWORD'),
        host = config.get('database', 'DB_HOST'),
        port = config.get('database', 'DB_PORT'),
        database = config.get('database', 'DB_NAME')
    )