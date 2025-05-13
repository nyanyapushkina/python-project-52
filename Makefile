PORT ?= 8000

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

.PHONY: install test lint check build start dev run test-coverage render-start