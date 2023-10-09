.PHONY: image start restart k dev prod export clean help
.DEFAULT_GOAL := help

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

export:
	@poetry lock --no-update
	@poetry export -f requirements.txt --output requirements.txt --without-hashes

clean:
	@docker compose -p ${COMPOSE_SERVICE_NAME} down
	@kubectl delete -f ${K8S_APP} 2> /dev/null || echo "No k8s resource found"
	@docker container prune -f
	@docker image rm -f ${IMAGE_NAME}
	@docker image prune -f

# Show help
help:
	@echo ""
	@echo "Usage:"
	@echo "    make [target]"
	@echo ""
	@echo "Targets:"
	@awk '/^[a-zA-Z\-_0-9]+:/ \
	{ \
		helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 2, RLENGTH); \
			printf "\033[36m%-22s\033[0m %s\n", helpCommand,helpMessage; \
		} \
	} { lastLine = $$0 }' $(MAKEFILE_LIST)
