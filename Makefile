.DEFAULT_GOAL := help

.PHONY: $(shell perl -nle'print $$& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {print $$1}')

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'


test: ## runs tests
	docker-compose -f local.yml run django py.test -vv --cache-clear

build: ## builds django docker image
	docker-compose -f local.yml build django

logs: ## attach to production logs
	docker-compose -f local.yml logs --tail 100 -f

up: ## runs all docker containers
	docker-compose -f local.yml up --build -d

stop: ## stops all docker containers
	docker-compose -f local.yml stop

drop-db: stop ## drop the local database content
	docker-compose -f local.yml down
	docker volume rm weather_forecast_app_weather_forecast_app_local_postgres_data weather_forecast_app_weather_forecast_app_local_postgres_data_backups

down: ## removes all docker containers
	docker-compose -f local.yml down

db: ## runs db docker containers
	docker-compose -f local.yml up postgres

createapp: ## create a new Django app. Usage: make createapp name=name_of_the_app
	cd weather_forecast_app && python ../manage.py startapp $(name)
	find . -print | grep -i "./weather_forecast_app/$(name)" | xargs -d '\n' sudo chown eracle:eracle

migrations: ## make migration files
	docker-compose -f local.yml run django python manage.py makemigrations
	find . -print | grep -i "./weather_forecast_app/.*/migrations/" | xargs -d '\n' sudo chown eracle:eracle

node:  ## lanches node locally
	docker-compose -f local.yml up --build node

node-local-build: ## rebuilds local node
	docker ps -a | grep -E "node|weather_forecast_app" | awk '{print $1}' | xargs docker rm -f
	docker images | grep -E "node|weather_forecast_app" | awk '{print $3}' | xargs docker rmi -f
	docker-compose -f local.yml build --no-cache node

node-webpack-build: ## prepare bundles for production
	sudo rm -rf weather_forecast_app/static/webpack_bundles/*
	docker-compose -f local.yml run node npm run build
	sudo chown eracle:eracle -R weather_forecast_app/static/webpack_bundles/
