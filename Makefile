IMAGE_NAME="pplmx/fastapi_sample"
COMPOSE_SERVICE_NAME="demo"

image:
	docker image build -t ${IMAGE_NAME} .

start:
	docker compose -p ${COMPOSE_SERVICE_NAME} up -d

restart:
	docker compose -p ${COMPOSE_SERVICE_NAME} down
	docker compose -p ${COMPOSE_SERVICE_NAME} up -d

dev: image restart
