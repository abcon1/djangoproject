from flask_restful import Api

from system_service.api.v1.common.authorization import is_authorized
from system_service.api.v1.common.errors import UnauthorizedError
from system_service.api.v1.resources.devices.devices import Devices, Device
from system_service.app import logger, app


def create(api: Api):
    api.add_resource(Devices, "/api/v1/devices")
    api.add_resource(Device, "/api/v1/devices/<int:id>")

    logger.info("[API] Loaded \'devices\' resource.")


@app.before_request
def authorize():
    if is_authorized() is False:
        raise UnauthorizedError
