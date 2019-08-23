from http import HTTPStatus

from flask import jsonify


class APIException(Exception):
    status_code = HTTPStatus.UNAUTHORIZED

    def __init__(self, message="Error while processing request", status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        print(rv["message"])
        return rv


class InternalServerError(APIException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR


class UnauthorizedError(APIException):
    status_code = HTTPStatus.UNAUTHORIZED


class SchemaValidationError(APIException):
    status_code = HTTPStatus.BAD_REQUEST


class DeviceAlreadyExistsError(APIException):
    status_code = HTTPStatus.CONFLICT

class UserAlreadyExistsError(APIException):
    status_code = HTTPStatus.CONFLICT


class DeviceNotExistsError(APIException):
    status_code = HTTPStatus.NOT_FOUND


class UserNotExistsError(APIException):
    status_code = HTTPStatus.NOT_FOUND


class UserQuotaFullError(APIException):
    status_code = HTTPStatus.INSUFFICIENT_STORAGE


class BadRequestError(APIException):
    status_code = HTTPStatus.BAD_REQUEST


# errors = {
#     "InternalServerError": {"status": 500},
#     "UnauthorizedError": {"status": 401},
#     "SchemaValidationError": {
#         "message": "Request is missing required JSON values",
#         "error": 1,
#         "status": HTTPStatus.BAD_REQUEST,
#     },
#     "DeviceNotExistsError": {
#         "message": "Device with given id doesn't exists",
#         "error": 1,
#         "status": HTTPStatus.NOT_FOUND,
#     },
#     "DeviceAlreadyExistsError": {
#         "message": "Device with given name already exists",
#         "error": 1,
#         "status": HTTPStatus.NO_CONTENT,
#     },
#     "DeviceNotExistsError": {
#         "message": "Device with given id doesn't exists",
#         "error": 1,
#         "status": HTTPStatus.NOT_FOUND,
#     },
#     "UserNotExistsError": {
#         "message": "User with given id doesn' exists",
#         "error": 1,
#         "status": HTTPStatus.NOT_FOUND,
#     },
#     "UserQuotaFullError": {
#         "message": "Given device is already assigned to 3 users",
#         "error": 1,
#         "status": HTTPStatus.INSUFFICIENT_STORAGE,
#     },
#     "BadRequestError": {
#         "message": "Bad Request",
#         "error": 1,
#         "status": HTTPStatus.BAD_REQUEST,
#     },
# }
