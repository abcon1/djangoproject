from flask import Flask
from flask_restful import Api

from api.v1 import routes
from api.v1.common.errors import errors
from app import logger


def create(app: Flask):
    api = Api(app, catch_all_404s=False, errors=errors)
    logger.info('[API] Started.')
    routes.create(api)
    return api
