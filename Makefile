.PHONY: run build

build:
	docker build --rm -t puckel/docker-airflow:1.9.0-4 .

run: build
	docker-compose -f docker-compose.yml up -d
	@echo airflow running on http://localhost:8080

kill:
	@echo "Killing docker-airflow containers"
	docker kill $(shell docker ps -q --filter ancestor=puckel/docker-airflow:1.9.0-4) $(shell docker ps -q --filter ancestor=postgres:9.6)

tty:
	docker exec -i -t $(shell docker ps -q --filter ancestor=puckel/docker-airflow:1.9.0-4) /bin/bash

root:
	docker exec -u 0 -ti $(shell docker ps -q --filter ancestor=puckel/docker-airflow:1.9.0-4) /bin/bash

restart: kill run
