.PHONY: help install install-dev test lint format clean build publish docs

help:
	@echo "PyPSA Explorer - Development Commands"
	@echo ""
	@echo "install        Install package"
	@echo "install-dev    Install package with development dependencies"
	@echo "test          Run tests with pytest"
	@echo "test-cov      Run tests with coverage report"
	@echo "lint          Run linting (ruff + mypy)"
	@echo "format        Format code (black + ruff)"
	@echo "clean         Remove build artifacts"
	@echo "build         Build distribution packages"
	@echo "publish       Publish to PyPI (requires TWINE credentials)"
	@echo "docs          Build documentation"
	@echo "run           Run dashboard with demo network"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

test-cov:
	pytest --cov=pypsa_explorer --cov-report=html --cov-report=term-missing

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff format src/ tests/
	ruff check src/ tests/ --fix

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	twine check dist/*
	twine upload dist/*

docs:
	cd docs && make html

run:
	pypsa-explorer
