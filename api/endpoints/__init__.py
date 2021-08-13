from endpoints.gateway.resource import GatewayResource
from endpoints.meter_data.resource import MeterDataResource, MeterDataOverview
from endpoints.sensor_data.resource import SensorDataResource
from endpoints.sensor.resource import SensorResource
from endpoints.user.resource import UserResource, LoginResource
from endpoints.device.resource import DeviceResource
from endpoints.control.resource import ControlResource
from endpoints.appliances.resource import AppliancesResource
from endpoints.health.resource import HealthResource
from endpoints.pir_records.resource import PirRecordsResource


RESOURCES = {
    "gateway": GatewayResource,
    "meter_data": MeterDataResource,
    "meter_data/overview": MeterDataOverview,
    "sensor_data": SensorDataResource,
    "user": UserResource,
    "login": LoginResource,
    "device": DeviceResource,
    "control": ControlResource,
    "health": HealthResource,
    "sensor": SensorResource,
    "appliance": AppliancesResource,
    "pir_records": PirRecordsResource,
}
