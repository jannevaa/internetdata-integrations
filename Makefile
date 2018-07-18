.PHONY: run build

build:
	docker build --rm -t puckel/docker-airflow .

run: build
	docker-compose -f docker-compose-LocalExecutor.yml up -d
	@echo airflow running on http://localhost:8080

kill:
	@echo "Killing docker-airflow containers"
	docker kill $(shell docker ps -q --filter ancestor=puckel/docker-airflow:1.9.0-4) $(shell docker ps -q --filter ancestor=postgres:9.6)

tty:
	docker exec -i -t $(shell docker ps -q --filter ancestor=puckel/docker-airflow:1.9.0-4) /bin/bash

update_dags:
	docker cp dags/*.py $(shell docker ps -q --filter ancestor=puckel/docker-airflow:1.9.0-4):/usr/local/airflow/dags/
