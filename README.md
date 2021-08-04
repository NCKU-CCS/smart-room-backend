# smart room - backend

![Integration](https://github.com/NCKU-CCS/smart-room-backend/workflows/Integration/badge.svg)

![Build](https://github.com/NCKU-CCS/smart-room-backend/workflows/Build/badge.svg)

Smart Room Control and Data Collect Service

+ [api](./api): Main API Server
    + Flask API Server
    + Data Collection
    + Device Control
    + User Management

+ Redis Server

+ Grafana

+ Relative Projects

    + [Database](https://github.com/NCKU-CCS/smart-room-schema)

    + [front end](https://github.com/NCKU-CCS/smart-room-frontend)

    + [controller](https://github.com/NCKU-CCS/smart-room-controller): A/C Controller
        + Socket Server
        + Receive Command
        + Token Authentication
        + IR Remote Control

    + [sensor](https://github.com/NCKU-CCS/smart-room-sensor): Sensors
        + Data Collectction
        + Thermo Sensor
        + Smart Meter
        + CT Sensor

## API Document

Document: [apiary.apib](./apiary.apib)

Online Document: [smart-room document](https://smartroom1.docs.apiary.io/#)

## Getting Started

### Prerequisites

- python 3.7
- docker 19.03.6

### DB Service
[Database](https://github.com/NCKU-CCS/smart-room-schema)

Update submodule files
```sh
git submodule update --init --remote
```

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
python api/manage.py db init
python api/manage.py db upgrade
```

5. (Optional) Shut down external services
```sh=
make service_down
```

6. (Optional) Version freeze to generate `requirements.txt`
```sh=
pipenv lock --requirements > requirements.txt
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

## Usage

### Add a sensor with new gateway
1. Add Gateway
2. Add Sensor
3. Start to Upload Data
