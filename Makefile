COMPOSE = docker-compose
PROJECT_FILE = docker-compose.dev.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_FILE = docker_compose/app.yaml
EXEC = docker exec -it
ENV = --env-file .env
APP_CONTAINER = app
DB_CONTAINER = db


.PHONY: storages-up
storages-up:
	${COMPOSE} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: storages-down
storages-down:
	${COMPOSE} -f ${STORAGES_FILE} down

.PHONY: postgres-psql
postgres-psql:
	${EXEC} ${DB_CONTAINER} psql

.PHONY: app-up
app-up:
	${COMPOSE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-up:
	${COMPOSE} -f ${APP_FILE} down

.PHONY: project-up
project-up:
    ${COMPOSE} -f ${PROJECT_FILE} ${ENV} up --build -d

.PHONY: project-down
project-down:
    ${COMPOSE} -f ${PROJECT_FILE} down

.PHONY: migrate
migrate:
    ${EXEC} ${APP_CONTAINER} alembic upgrade head

.PHONY: makemigration
makemigration:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate

.PHONY: tests
tests:
    ${EXEC} ${APP_CONTAINER} pytest

.PHONY: lint
lint:
    ${EXEC} ${APP_CONTAINER} ruff check

.PHONY: format
format:
    ${EXEC} ${APP_CONTAINER} ruff format && ruff format