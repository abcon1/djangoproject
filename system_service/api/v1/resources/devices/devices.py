from database import models
from app import db, logger

from flask_restful import Resource
from flask import request, jsonify, make_response
from mongoengine.errors import NotUniqueError

from api.v1.common.errors import (InternalServerError,
                                  DeviceNotExistsError,
                                  DeviceAlreadyExistsError,
                                  SchemaValidationError)


class Device(Resource):

    def put(self, nic_id):
        try:
            device = models.Device.objects.get(id=nic_id)
        except Exception:
            raise DeviceNotExistsError()

        request_json = request.get_json(force=True)
        if "name" not in request_json:
            raise SchemaValidationError()
        device.name = request_json["name"]

        try:
            device.save()
        except NotUniqueError:
            raise DeviceAlreadyExistsError()

        return None, 200

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

    def post(self):
        request_json = request.get_json(force=True)

        self.__add_devices(request_json)

        return None, 200

    def __add_devices(self, _request):
        if "devices" not in _request:
            raise SchemaValidationError()
        devices = _request["devices"]
        for device in devices:
            try:
                if "name" not in device:
                    raise SchemaValidationError()

                name = device["name"]
                d = models.Device(name=name, assigned_to=0)
                d.save()

            except NotUniqueError:
                raise DeviceAlreadyExistsError(
                    "Device with name {} already exists".format(name)
                )
