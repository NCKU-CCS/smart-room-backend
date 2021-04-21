# smart room

![Integration](https://github.com/NCKU-CCS/smart-room-backend/workflows/Integration/badge.svg)

![Build](https://github.com/NCKU-CCS/smart-room-backend/workflows/Build/badge.svg)

Smart Room Control and Data Collect Service

+ [api](./api): Main API Server
    + Flask API Server
    + Data Collect
    + Device Control
    + User Management

+ [controller](./controller): A/C Controller
    + Socket Server
    + Receive Command
    + Token Authentication
    + IR Remote Control

+ [sensor](./sensor): Sensors
    + Python3.7 Script and Arduino Script
    + Data Collect
        + [meter.py](./sensor/meter.py): Smart Meter via Modbus Communication
        + [thermo_sensor.py](./sensor/thermo_sensor.py): DHT Temperature and Humidity Sensor
        + [sct-013.ino](./sensor/Arduino/sct013.ino): SCT-013 GET Current Data using Arduino
        + [read_arduino.py](./sensor/read_arduino.py): Read CT data from Arduino via serial signal


## API Document

Document: [apiary.apib](./apiary.apib)

Online Document: [smart-room document](https://smartroom1.docs.apiary.io/#)

## Getting Started

### Prerequisites

- python 3.7
- docker 19.03.6


### Running Development

1. Create environment file
```sh=
cp sample.env .env
```

2. Installing Packages & Entering environment
```sh=
make dev
pipenv shell
```

3. Starting external components
```sh=
make service_up
```

4. Migrating database
```sh=

```

5. (Optional) Shut down external services
```sh=
make service_down
```

### Running Production

1. build docker image
```sh
make build
```

2. update the .env file
3. run docker-compose
```sh
docker-compose up -d
```

### Database Migration

Init:
`python api/manage.py db init`

To make migration change:
`python api/manage.py db migrate`

To apply migration changes to database:
`python api/manage.py db upgrade`

To stamp existing database to certain revision version
`python api/manage.py db stamp {revision ID / head}`

command reference: [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/#command-reference)
