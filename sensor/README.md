# smart room - sensor

Smart Room Sensors

+ [Thermo sensor](./thermo_sensor.py)
    + DHT11, DHT22 Thermo Data
+ [Smart Meter](./meter.py)
    + Smart Meter Data
+ [CT Sensor](./read_arduino.py)
    + CT Sensor Data

## Getting Started

### Prerequisites

- python 3.7

### Config

Update `.env` setting file
```sh
cp env.sample .env
# update .env file
```

### Running

Installing Packages
```sh
pip3 install requests, python-dotenv, dataclasses-json
```

#### meter
Read data from Smart Meter via modbus.

```sh
# minimalmodbus for modbus communication
pip3 install minimalmodbus
python3 meter.py
```

#### Thermo sensor
Read data from DHT Sensor.

Customize `Adafruit_DHT` package: make DHT11 data accuracy to one decimal place.

```sh
python3 thermo_sensor.py
```

#### CT sensor
Read data from CT sensor from Arduino via serial signal.

*CT Sensor* --Aanlog Signal-> *Arduino* --Serial Signal--> *Raspberry pi* ---> *Data Center*

```sh
pip3 install pyserial
python3 read_arduino.py
```

### Save Data

[save_data.py](./save_data.py) include `upload_data` function to upload data to data center via HTTP POST request.
