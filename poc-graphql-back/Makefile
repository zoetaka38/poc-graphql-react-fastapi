APP_ENV := local
MIGRATION_MESSAGE := migration_message

build:
	STAGE=$(APP_ENV) docker compose build

run:
	STAGE=$(APP_ENV) docker compose up


makemigrations:
	STAGE=$(APP_ENV) docker-compose run --rm graphql-api alembic revision --autogenerate -m "create table"

migrate:
	STAGE=$(APP_ENV) docker-compose run --rm graphql-api alembic upgrade head