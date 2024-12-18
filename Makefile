REGISTRY=ghcr.io/almazkun
IMAGE_NAME=djitt
CONTAINER_NAME=djitt-container
VERSION=0.1.0

ENV=pipenv run
CMD=python

k=.


build:
	docker build -t $(REGISTRY)/$(IMAGE_NAME):$(VERSION) .

run:
	docker run \
		-it \
		-p 8000:8000 \
		--rm --name $(CONTAINER_NAME) $(REGISTRY)/$(IMAGE_NAME):$(VERSION)