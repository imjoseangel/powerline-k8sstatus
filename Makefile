# Current version
# VERSION ?= 1.0.3

.DEFAULT_GOAL:=help

PATH  := $(PATH):$(PWD)/bin
SHELL := env PATH=$(PATH) /bin/bash
OS    = $(shell uname -s | tr '[:upper:]' '[:lower:]')
ARCH  = $(shell uname -m | sed 's/x86_64/amd64/')
OSOPER   = $(shell uname -s | tr '[:upper:]' '[:lower:]' | sed 's/darwin/apple-darwin/' | sed 's/linux/linux-gnu/')
ARCHOPER = $(shell uname -m )

.PHONY: help clean build install uninstall

help:  ## Display this help
		@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

all: build

clean: ## Cleanup the project folders
		$(info Make: Cleaning up things)
		python setup.py clean

build: clean ## Build and upload the project to Pypi
		$(info Make: Build and upload the project to Pypi)
		python setup.py clean
		python setup.py sdist bdist_wheel
		twine upload dist/*

install: ## Install in editable mode
		$(info Make: Install in editable mode)
		pip install -e ./

uninstall: ## Uninstall package
		$(info Make: Uninstall package.)
		pip uninstall powerline_k8sstatus

test: ## Run unit tests
		$(info Make: Run unit tests.)
		pytest
