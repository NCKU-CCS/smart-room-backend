PKG=api

.PHONY: all clean version init flake8 pylint lint test coverage

init: clean
	pipenv --python 3.7
	pipenv install
	git submodule update --init --remote

dev: init
	pipenv install --dev
	# pipenv run pre-commit install -t commit-msg

service_up:
	cd database && make service_up && sleep 1 && make migrate
	docker-compose run -d grafana && \
	docker-compose run -d redis

service_down:
	cd database && make service_down
	docker-compose down && \
	docker volume rm redis_data grafana_data

commit:
	pipenv run cz commit

flake8:
	pipenv run flake8

pylint:
	pipenv run pylint $(PKG) --rcfile=setup.cfg

black:
	pipenv run black $(PKG) --skip-string-normalization -l 120

isort:
	pipenv run isort --recursive --apply

lint: flake8 pylint

build:
	docker-compose build

run:
	cd ${PKG} && pipenv run python app.py

clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete

db_migrate:
	pipenv run python ${PKG}/manage.py db migrate

db_upgrate:
	pipenv run python ${PKG}/manage.py db upgrade
