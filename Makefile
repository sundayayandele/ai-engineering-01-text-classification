.PHONY: install test lint train run docker-build

install:
	python -m pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check .

train:
	python scripts/train.py

run:
	uvicorn app.main:app --reload

docker-build:
	docker build -t text-classifier:local .
