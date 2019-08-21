from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from api.v1.common.errors import (InternalServerError,
                                  DeviceNotExistsError,
                                  UserNotExistsError,
                                  UserQuotaFullError,
                                  DeviceAlreadyExistsError,
                                  SchemaValidationError)
from app import db, logger

from database import models


class User(Resource):
    def post(self):
        request_json = request.get_json(force=True)

        self.__add_user(request_json)

        return None, 200

    def __add_user(self, _request):
        password = _request["password"]
        # hashed_password = generate_password_hash(password, method='sha256')
        user = models.User(
            username=_request["username"],
            password=password,
            devices=[device for device in _request["devices"]]
        )
        user.save()


class AddDevice(Resource):
    def put(self, nic_id):

        request_json = request.get_json(force=True)
        if "devices" not in request_json:
            raise SchemaValidationError()
        devices = request_json["devices"]
        self.__add_device(nic_id, devices)

        return None, 200

    def __add_device(self, _id_user, devices):
        try:
            user = models.User.objects.get(id=_id_user)
        except Exception:
            raise UserNotExistsError()

        existing_devices = user.devices

        for device in devices:
            # chech if the device is already in user devices list
            if device in existing_devices:
                raise DeviceAlreadyExistsError()

            try:
                print(device)
                models.Device.objects.get(id=device)
            except Exception:
                raise DeviceNotExistsError()

            # try:
            models.User.objects(id=_id_user).update_one(push__devices=device)
            models.Device.objects(id=device).update_one(inc__assigned_to=1)
            # except Exception:
            #     raise UserQuotaFullError()