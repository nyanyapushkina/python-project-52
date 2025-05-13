PORT ?= 8000

install:
	uv sync

build:
	chmod +x ./build.sh
	./build.sh

render-start:
    gunicorn task_manager.wsgi

.PHONY: install test lint check build start dev run test-coverage render-start