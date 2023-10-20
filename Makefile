.PHONY: image start restart k dev prod export clean help
.DEFAULT_GOAL := help

IMAGE_NAME="pplmx/fastapi_sample"
COMPOSE_SERVICE_NAME="demo"
K8S_APP="k8s/app.yml"

# Build image
image:
	@docker image build -t ${IMAGE_NAME} .

# Start services
start:
	@docker compose -p ${COMPOSE_SERVICE_NAME} up -d

# Stop services
stop:
	@docker compose -p ${COMPOSE_SERVICE_NAME} down

# Restart services
restart: stop start

# Deploy to k8s
k:
	kubectl apply -f ${K8S_APP}

# Run dev server
dev: image restart

# Run prod server
prod: image k

# Export requirements
export:
	@poetry lock --no-update
	@poetry export -f requirements.txt --output requirements.txt --without-hashes

# Clean up
clean:
	@docker compose -p ${COMPOSE_SERVICE_NAME} down -v
	@kubectl delete -f ${K8S_APP} 2> /dev/null || echo "No k8s resource found"
	@docker container prune -f

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
