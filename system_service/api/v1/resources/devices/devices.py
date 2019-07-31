from flask_restful import Resource
from flask import request

from system_service.api.v1.common.errors import InternalServerError
from system_service.app import db, logger


class Device(Resource):
    def delete(self, _id):
        self.__remove_device(_id)

        return None, 200

    def __remove_device(self, _id):
        # TODO: remove device from database.
        # in case of an error:
        # - raise relevant exception from database
        # - catch it here and raise InternalServiceError to client
        pass


class Devices(Resource):
    def get(self):
        # return all devices to client
        pass

    def post(self):
        # TODO: add request validation
        # raise SchemaValidationError to client in case of bad request

        _request = None # TODO: Assign validated request to _request
        self.__add_devices(_request)

        return None, 200

    def __add_devices(self, _request):
        devices = [tuple(device.values()) for device in _request['devices']]

        try:
            # TODO: add devices into database,
            # make sure there are no duplicated devices
            pass
        except Exception:
            raise InternalServerError(
                "[API] One of the added devices is already exists.")