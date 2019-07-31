from pathlib import Path

from flask import Flask

from system_service.logger import load_logger

app = Flask(
    __name__,
    static_folder=str(Path(__file__).resolve().parents[1]/'static')
)

logger = load_logger(app)
api = None


def run(*args, **kwargs):
    app.run(*args, **kwargs)

