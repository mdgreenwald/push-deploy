.PHONY: build

default: build

help:
	@echo "usage: make <command>"
	@echo ""
	@echo "A set of Makefile commands designed to manipulate the"
	@echo "development environment. The default command is 'build', meaning that"
	@echo "running 'make' without any arguments is the same as running 'make build'."
	@echo ""
	@echo "Commands:"
	@echo "  build"
	@echo "    Builds the Push-Deploy container."

build:
	@docker build -t push-deploy/latest -f Dockerfile .

%:
	@:
