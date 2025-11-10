
DOCKER=docker
IMGTAG=img.stelar.gr/stelar/gilgamesh-summarizer:latest
IMGPATH=.
DOCKERFILE=$(IMGPATH)/Dockerfile

.PHONY: all build push


all: build push

build:
	$(DOCKER) build -f $(DOCKERFILE) $(IMGPATH) -t $(IMGTAG)

push:
	$(DOCKER) push $(IMGTAG)

