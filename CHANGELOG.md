## 0.1.0 (2021-08-04)

### Refactor

- Update submodule and configs
- Refactor import route
- Update build
- Remove unused docker-compose
- **start_up.py**: fix linter issue
- Update Dockerfile to import migrations
- Update related API models import
- Add __init__.py to make it become submodule
- Remove unused README
- Move models to migration folder
- Update import order and default template
- Separate migration script from flask
- **meter_data**: refactor get data
- **meter_data**: mr issues
- **meter_data**: update timezone use TZ_OFFSET
- Remove migration code currently
- Use pure sqlalchemy to control queries
- Start refactoring
- **appliances**: refactor variable name and make mode_judgment as func
- **device,-sensor**: add room to args
- **appliances**: update form
- Remove requirements.txt
- Split some modules to other repositories
- **appliances**: fix issues
- Resolve thread issues
- Move service out of services/ folder
- Refine docker compose order
- Update README.md and default environment variable
- Update service init/shutdown make
- Refactor strucutre
- Refine folder strucutre

### Fix

- **GET-meter_data**: fix outdoor thermo sensor
- **meter_data**: change thermo sensor of overview
- **meter_data-and-config**: fix mr issue
- Fix redis init exception
- **device**: add `location`

### Feat

- **meter_data**: GET meter_data
- **meter_data/overview**: add overview
- **appliances**: get appliances latest state
- **device,-sensor**: add room column

## 0.0.2 (2021-04-19)

### Refactor

- Update CICD
- Resolve merge conflict

## 0.0.1 (2021-04-19)

### Refactor

- **sensor/meter.py**: decode float data with minimalmodbus
- **endpoints**: formatting: follow linter and black
