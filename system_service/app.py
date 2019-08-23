from pathlib import Path

from flask import Flask
from flask_cors import CORS

from logger import load_logger

CORS_ALLOWED_ORIGINS_LIST = ["http://127.0.0.1:8080", "http://localhost:8080", "http://127.0.0.1:80", "http://localhost:80"]

app = Flask(__name__, static_folder=str(Path(__file__).resolve().parents[1] / "static"))

logger = load_logger(app)
api = None
db = None

def run(*args, **kwargs):
    global api
    global db

    app.config["MONGODB_SETTINGS"] = {
        "host": "mongodb+srv://tests:tests12345@cluster0-sf4tf.mongodb.net"
    }

    app.secret_key = "a26be1a658027b1749da74befe4c25ca"

    from database import database

    db = database.create(app)

    logger.info("[SERVICE] Started.")

    from api import api

    api = api.create(app)

    CORS(app, origins=CORS_ALLOWED_ORIGINS_LIST,
         supports_credentials=True)

    app.run(*args, **kwargs)
