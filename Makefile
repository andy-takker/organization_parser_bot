PYTHON_VERSION := 3.12
PROJECT_NAME = organization_parser

develop: clean-dev
	python${PYTHON_VERSION} -m venv .venv
	.venv/bin/pip install -U pip uv
	.venv/bin/uv sync
	.venv/bin/pre-commit install

develop-ci:
	pip install -U pip uv
	uv sync

lint-ci: ruff-ci mypy-ci  ##@Linting Run all linters in CI

ruff-ci: ##@Linting Run ruff
	ruff check ./$(PROJECT_NAME)

mypy-ci: ##@Linting Run mypy
	mypy ./$(PROJECT_NAME) --config-file ./pyproject.toml

clean-dev:
	rm -rf .venv

local:
	docker compose -f docker-compose.dev.yaml up --build --force-recreate --remove-orphans

local-dev:
	docker compose -f docker-compose.dev.yaml down