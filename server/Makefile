.PHONY: publish image run

version ?= latest
IMAGE = leocbs/openhack-server:$(version)

publish: image
	docker push $(IMAGE)

image:
	docker build -t $(IMAGE) .

run: image
	docker run --rm -p 5000:5000 leocbs/openhack-server
