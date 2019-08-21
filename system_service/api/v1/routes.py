from flask_restful import Api

from api.v1.common.authorization import is_authorized
from api.v1.common.errors import UnauthorizedError
from api.v1.resources.devices.devices import Devices, Device
from api.v1.resources.users.users import User, AddDevice
from app import logger, app


def create(api: Api):
    api_prefix = "/api/v1"
    device_id = "<string:nic_id>"
    user_id = "<string:nic_id>"

    api.add_resource(Devices, "{}/devices".format(api_prefix))
    api.add_resource(Device, "{}/devices/{}".format(api_prefix, device_id))

    logger.info("[API] Loaded \'devices\' resource.")

    api.add_resource(User, "{}/users".format(api_prefix))

    logger.info("[API] Loaded \'users\' resource.")

    api.add_resource(AddDevice, "{}/users/{}/add_device".format(api_prefix, user_id))

    logger.info("[API] Loaded \'users add_device\' resource.")


@app.before_request
def authorize():
    if is_authorized() is False:
        raise UnauthorizedError
