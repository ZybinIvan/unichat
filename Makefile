DC = docker compose
APP_CONTAINER = unichat
DB_CONTAINER = mediais_db
ENV_FILE = .env

EXEC = docker exec -it

.PHONY: app-build
app-build:
	${DC} build

.PHONY: app
app:
	${DC} up -d


.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} alembic upgrade head

.PHONE: alembic-head
alembic-head:
	${EXEC} ${APP_CONTAINER} alembic history

.PHONY: makemigrations
makemigrations:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate

.PHONY: inside
inside:
	${EXEC} ${APP_CONTAINER} sh

.PHONY: psql
psql:
	${EXEC} ${DB_CONTAINER} psql -U mediais backendis

.PHONY: db-logs
db-logs:
	docker logs ${DB_CONTAINER}


.PHONY: create-app
create-app:
	${EXEC} ${APP_CONTAINER} python -m src.core.scripts.make_app