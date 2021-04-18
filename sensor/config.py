import os

from dotenv import load_dotenv


load_dotenv()

# Thermo Sensor
DHT_PIN = int(os.getenv("DHT_PIN", "27"))
# DHT_TYPE (1)DHT11: DHT11; (2)DHT22: AM2302
DHT_TYPE = os.getenv("DHT_TYPE", "AM2302")

# Smart Meter
MODBUS_PORT = os.getenv("MODBUS_PORT", "/dev/ttyUSB0")

# CT Sensor
ARDUINO_PORT = os.getenv("ARDUINO_PORT", "/dev/ttyUSB0")
CT_MAPPING = ["WWW", "VLDB_E", "VLDB_W", "LAB_E", "LAB_W", "KDD"]

# Upload
SENSOR = os.getenv("SENSOR", "")
ENDPOINT = os.getenv("ENDPOINT", "http://10.8.2.101:5000/")
TOKEN = os.getenv("TOKEN", "")

# Log only
GATEWAY = os.getenv("GATEWAY", "")
