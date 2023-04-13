.PHONY: help

help: ## This help dialog.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

LOCAL_COMPOSE_FILE ?= ./docker/compose/docker-compose.local.yml

# ----------------------------------------------------------------------------------------------------------------------
#                                           BUILD
# ----------------------------------------------------------------------------------------------------------------------

poetry-requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

build:  ## Build docker image (Run with sudo)
	docker-compose -f ${LOCAL_COMPOSE_FILE} -p todo build

# ----------------------------------------------------------------------------------------------------------------------
#                                           LOCAL
# ----------------------------------------------------------------------------------------------------------------------
up:  ## Up docker-compose
	docker-compose -f ${LOCAL_COMPOSE_FILE} -p todo up -d

down:  ## Down docker-compose
	docker-compose -f ${LOCAL_COMPOSE_FILE} -p todo down -v --remove-orphans

shp:  ## Run shell_plus
	docker-compose -f ${LOCAL_COMPOSE_FILE} -p todo exec app python manage.py shell_plus
