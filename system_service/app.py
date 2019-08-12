from pathlib import Path

from flask import Flask
from flask_cors import CORS

from system_service.logger import load_logger

CORS_ALLOWED_ORIGINS_LIST = ["?"]

app = Flask(
    __name__,
    static_folder=str(Path(__file__).resolve().parents[1]/'static')
)

logger = load_logger(app)
api = None
db = None


def run(*args, **kwargs):
    from .database import database

    global api
    global db

    # TODO: add real database parameters
    # app.config['MONGODB_SETTINGS'] = {
    #     'db': 'db name here',
    #     'host': 'db host here (if host is uri - db name will taken from here)',
    #     'port': 'db port here',
    #     'username': 'db username here',
    #     'password': 'db password here'
    # }

    app.secret_key = "this is very secret"

    db = database.create(app)

    logger.info('[SERVICE] Started.')

    from .api import api

    api = api.create(app)

    CORS(app, origins=CORS_ALLOWED_ORIGINS_LIST,
         supports_credentials=True)

    app.run(*args, **kwargs)

