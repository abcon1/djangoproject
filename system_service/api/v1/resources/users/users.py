from flask_restful import Resource, reqparse
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

from api.v1.common.errors import (
    InternalServerError,
    DeviceNotExistsError,
    UserNotExistsError,
    UserQuotaFullError,
    DeviceAlreadyExistsError,
    BadRequestError,
    SchemaValidationError,
    UserAlreadyExistsError,
)
from app import db, logger

from database import models

auth = HTTPBasicAuth()


class User(Resource):
    def post(self):
        request_json = request.get_json(force=True)

        created_user = self.__add_user(request_json)

        return {"created_user": created_user}, 201

    def __add_user(self, _request):
        parser = reqparse.RequestParser()

        parser.add_argument(
            "username", type=str, help="Username for new user", location="json"
        )

        parser.add_argument(
            "password", type=str, help="Password for user", location="json"
        )

        if "devices" not in _request:
            raise BadRequestError(
                "List of device id to be assigned for user, pass empty list for None"
            )

        args = parser.parse_args()
        password = args["password"]
        hashed_password = generate_password_hash(password, method="sha256")

        user = models.User(
            username=args["username"],
            password=hashed_password,
            devices=_request["devices"],
        )
        try:
            user.save()
        except Exception:
            raise UserAlreadyExistsError("User with given username already exists")
        return user.to_json()


class AddDevice(Resource):
    @auth.login_required
    def put(self, nic_id):

        request_json = request.get_json(force=True)
        if "devices" not in request_json:
            raise SchemaValidationError()
        devices = request_json["devices"]
        self.__add_device(nic_id, devices)

        return None, 200

    def __add_device(self, _user_id, devices):
        try:
            user = models.User.objects.get(id=_user_id)
        except Exception:
            raise UserNotExistsError()

        existing_devices = user.devices

        for device in devices:
            # chech if the device is already in user devices list
            if device in existing_devices:
                raise DeviceAlreadyExistsError()

            add_device = None
            try:
                add_device = models.Device.objects.get(id=device)
            except Exception:
                raise DeviceNotExistsError()

            if add_device.assigned_to == 3:
                raise UserQuotaFullError(
                    "Can't assign decive {} to more than 3 users".format(add_device.id)
                )

            models.User.objects(id=_user_id).update_one(push__devices=device)
            try:
                models.Device.objects(id=device).update_one(inc__assigned_to=1)
            except Exception:
                raise UserQuotaFullError()


@auth.verify_password
def verify_password(username, password):
    user = models.User.objects(username=username).first()
    if not user or not user.check_password(password):
        return False
    return True
