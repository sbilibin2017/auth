all: fix lint build-dev build-prod up-dev up-prod down-dev down-prod prune

SRC = src/
TESTS_FUNCTIONAL = tests/functional
# TESTS_UNIT_AUTH = ...
# TESTS_UNIT_USER = ...
# TESTS_UNIT_ROLE = ...
# TESTS_UNIT_PERMISSION = ...

install:
	poetry install

uninstall:
	rm -rf ./.venv/
	rm poetry.lock

fix:
	poetry run autoflake -r --remove-all-unused-imports --remove-unused-variables --remove-unused-variables --in-place --ignore-init-module-imports ${SRC}
	poetry run black ${SRC}
	poetry run isort ${SRC}	
	poetry run toml-sort --in-place pyproject.toml	

lint:
	poetry run flake8 ${SRC}
	poetry run pyright ${SRC}	

# test:
# 	poetry run pytest ${TESTS_UNIT_AUTH} -W ignore::DeprecationWarning
# 	poetry run pytest ${TESTS_UNIT_USER} -W ignore::DeprecationWarning
# 	poetry run pytest ${TESTS_UNIT_ROLE} -W ignore::DeprecationWarning
# 	poetry run pytest ${TESTS_UNIT_PERMISSION} -W ignore::DeprecationWarning
# 	poetry run pytest ${TESTS_FUNCTIONAL} -W ignore::DeprecationWarning
# 	poetry run pytest --cov=${SRC} -W ignore::DeprecationWarning
	

build:
	docker compose --env-file .env build

build-up:
	docker compose --env-file .env up --build

down:
	docker compose --env-file .env down

prune:
	docker container prune -f
	docker volume prune -f
	docker volume rm auth_cache_data auth_db_data







