from endpoints.gateway.resource import GatewayResource
from endpoints.meter_data.resource import MeterDataResource
from endpoints.sensor_data.resource import SensorDataResource
from endpoints.sensor.resource import SensorResource
from endpoints.user.resource import UserResource, LoginResource
from endpoints.device.resource import DeviceResource
from endpoints.control.resource import ControlResource
from endpoints.appliances.resource import AppliancesResource
from endpoints.health.resource import HealthResource


RESOURCES = {
    "gateway": GatewayResource,
    "meter_data": MeterDataResource,
    "sensor_data": SensorDataResource,
    "user": UserResource,
    "login": LoginResource,
    "device": DeviceResource,
    "control": ControlResource,
    "health": HealthResource,
    "sensor": SensorResource,
    "appliance": AppliancesResource,
}
