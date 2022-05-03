IMAGE_NAME="pplmx/fastapi_sample"
COMPOSE_SERVICE_NAME="demo"
K8S_APP="k8s/app.yml"

image:
	docker image build -t ${IMAGE_NAME} .

start:
	docker compose -p ${COMPOSE_SERVICE_NAME} up -d

restart:
	docker compose -p ${COMPOSE_SERVICE_NAME} down
	docker compose -p ${COMPOSE_SERVICE_NAME} up -d

k:
	kubectl apply -f ${K8S_APP}

dev: image restart

prod: image k

clean:
	docker compose -p ${COMPOSE_SERVICE_NAME} down
	kubectl delete -f ${K8S_APP} 2> /dev/null || echo "No k8s resource found"
	docker container prune -f
	docker image rm -f ${IMAGE_NAME}
	docker image prune -f
