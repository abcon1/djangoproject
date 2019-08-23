from flask_restful import Api
from flask import jsonify

from api.v1.common import errors
from api.v1.resources.devices.devices import Devices, Device
from api.v1.resources.users.users import User, AddDevice
from app import logger, app

from database import models


def create(api: Api):
    api_prefix = "/api/v1"
    device_id = "<string:nic_id>"
    user_id = "<string:nic_id>"

    api.add_resource(Devices, "{}/devices".format(api_prefix))
    api.add_resource(Device, "{}/devices/{}".format(api_prefix, device_id))

    logger.info("[API] Loaded 'devices' resource.")

    api.add_resource(User, "{}/users".format(api_prefix))

    logger.info("[API] Loaded 'users' resource.")

    api.add_resource(AddDevice, "{}/users/{}/add_device".format(api_prefix, user_id))

    logger.info("[API] Loaded 'users add_device' resource.")


@app.route("/about")
def about():
    total_devices = len(models.Device.objects())
    total_users = models.User.objects()

    result = {"total_devices": total_devices, "total_users": total_users}
    return {"data": result}, 200


@app.errorhandler(errors.APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
