dpl ?= deploy.env
include $(dpl)
export $(shell sed 's/=.*//' $(dpl))

# Get the short git commit hash:
VERSION=$(shell ./version.sh)

# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build -t $(APP_NAME) .

build-multi-arch: build-multi-arch-version build-multi-arch-latest

build-multi-arch-version: ## Build and upload container for amd64 and arm64 arch.
	docker buildx build --platform linux/amd64,linux/arm64 -t $(DOCKER_REPO)/$(APP_NAME):$(VERSION) --push .

build-multi-arch-latest: ## Build and upload container for amd64 and arm64 arch.
	docker buildx build --platform linux/amd64,linux/arm64 -t $(DOCKER_REPO)/$(APP_NAME):latest --push .

run: ## Run container on port configured in `deploy.env`
	docker run --rm -i -t -p=$(PORT):$(APP_PORT) --name="$(APP_NAME)" $(APP_NAME)

stop: ## Stop and remove a running container
	docker stop $(APP_NAME); docker rm $(APP_NAME)

# Docker tagging
tag: tag-version tag-latest ## Generate container tag for VERSION tag

tag-version: ## Generate container `version` tag
	@echo 'create tag' $(VERSION)
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

tag-latest: ## Generate container `latest` tag
	@echo 'create tag latest'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

# Docker upload

## Publish the `{version}` and `latest` tagged containers
upload: repo-login upload-latest upload-version 

upload-latest: tag-latest ## Publish the `latest` taged container
	@echo 'upload latest to $(DOCKER_REPO)'
	docker push $(DOCKER_REPO)/$(APP_NAME):latest

upload-version: tag-version ## Publish the `{version}` taged container
	@echo 'upload $(VERSION) to $(DOCKER_REPO)'
	docker push $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

lint:
	hadolint Dockerfile
#docker run --rm -i hadolint/hadolint < Dockerfile
	
k8s-deploy: # Deploy to kubernetes
# TBD


version: ## Output the current version
	@echo $(VERSION)

all: lint build

build-multi-arch: lint build-multi-arch-version build-multi-arch-latest