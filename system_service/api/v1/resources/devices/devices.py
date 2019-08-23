from database import models
from app import db, logger
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from flask_restful import Resource, reqparse
from flask import request, jsonify, make_response
from mongoengine.errors import NotUniqueError

from api.v1.common.errors import (
    InternalServerError,
    DeviceNotExistsError,
    DeviceAlreadyExistsError,
    SchemaValidationError,
)

auth = HTTPBasicAuth()


class Device(Resource):
    @auth.login_required
    def put(self, nic_id):
        try:
            device = models.Device.objects.get(id=nic_id)
        except Exception:
            raise DeviceNotExistsError("The device id doesn't exists")

        request_json = request.get_json(force=True)
        if "name" not in request_json:
            raise SchemaValidationError()
        device.name = request_json["name"]

        try:
            device.save()
        except NotUniqueError:
            raise DeviceAlreadyExistsError()

        return None, 200

    @auth.login_required
    def delete(self, nic_id):
        self.__remove_device(nic_id)

        return None, 200

    def __remove_device(self, _id):
        try:
            models.Device.objects(id=_id).delete()
        except Exception:
            raise DeviceNotExistsError()


class Devices(Resource):
    def get(self):
        devices = models.Device.objects()
        return make_response(jsonify(devices), 200)

    @auth.login_required
    def post(self):
        request_json = request.get_json(force=True)

        created_devices = self.__add_devices(request_json)

        return {"created_devices": created_devices}, 201

    def __add_devices(self, _request):
        if "devices" not in _request:
            raise SchemaValidationError()
        devices = _request["devices"]
        res_devices = []
        for device in devices:
            try:
                if "name" not in device:
                    raise SchemaValidationError()

                name = device["name"]
                d = models.Device(name=name, assigned_to=0)
                d.save()

                res_devices.append(d.to_json())
            except NotUniqueError:
                raise DeviceAlreadyExistsError(
                    "Device with name {} already exists".format(name)
                )

        return res_devices


@auth.verify_password
def verify_password(username, password):
    user = models.User.objects(username=username).first()
    if not user or not user.check_password(password):
        return False
    return True
