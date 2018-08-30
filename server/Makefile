version ?= latest
IMAGE = leocbs/openhack-server:$(version)

publish: image
	docker push $(IMAGE)

image:
	docker build -t $(IMAGE) .

run: image
	docker run --rm leocbs/openhack-server