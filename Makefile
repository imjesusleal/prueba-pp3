.PHONY: format
format:
	black .
	isort .
	flake8
	mypy api/ core/ db/ models/ services/ tests/  

.PHONY: dev
dev:
	fastapi dev main.py

.PHONY: test
test:
	pytest

.PHONY: test verbose
test:
	pytest -vs

.PHONY: install
install:
	pip install -r requirements.txt
	pre-commit install
