MSG ?= Migracion generada

.PHONY:
env:
	.\.venv\Scripts\activate

.PHONY: format
format:
	black .
	isort .
	flake8
	mypy api/ core/ db/ models/ services/ tests/  

.PHONY:
run:
	uvicorn main:app --reload

.PHONY:
migration: 
	alembic revision --autogenerate -m $"{MSG}"

.PHONY: 
db_update:
	alembic upgrade head

.PHONY: dev
dev:
	fastapi dev main.py

.PHONY: test
test:
	pytest -vv

.PHONY: install
install:
	pip install -r requirements.txt
	pre-commit install
