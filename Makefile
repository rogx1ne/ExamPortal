.PHONY: help venv install install-dev lint format test run migrate createsuperuser demo docker-up docker-down

VENV ?= .venv
PYTHON ?= $(VENV)/bin/python
PIP ?= $(VENV)/bin/pip
RUFF ?= $(VENV)/bin/ruff
PYTEST ?= $(VENV)/bin/pytest
PRECOMMIT ?= $(VENV)/bin/pre-commit

help:
	@echo "Targets:"
	@echo "  make venv            Create virtualenv in $(VENV)"
	@echo "  make install-dev     Install app + dev dependencies"
	@echo "  make lint            Run ruff checks"
	@echo "  make format          Auto-format and auto-fix"
	@echo "  make test            Run pytest"
	@echo "  make run             Run Django dev server"
	@echo "  make migrate         Apply migrations"
	@echo "  make createsuperuser Create admin user"
	@echo "  make demo            Seed demo data"
	@echo "  make docker-up       Start Docker services"
	@echo "  make docker-down     Stop Docker services (and volumes)"

venv:
	python3 -m venv $(VENV)
	$(PIP) install -U pip

install:
	$(PIP) install -r requirements.txt

install-dev: venv
	$(PIP) install -r requirements.txt -r requirements-dev.txt
	$(PRECOMMIT) install

lint:
	$(RUFF) format --check .
	$(RUFF) check .

format:
	$(RUFF) format .
	$(RUFF) check --fix .

test:
	$(PYTEST) --cov=accounts --cov=exams --cov=exam_portal --cov-report=term-missing --cov-fail-under=55

run:
	$(PYTHON) manage.py runserver

migrate:
	$(PYTHON) manage.py migrate

createsuperuser:
	$(PYTHON) manage.py createsuperuser

demo:
	$(PYTHON) manage.py seed_demo

docker-up:
	docker compose up --build

docker-down:
	docker compose down -v
