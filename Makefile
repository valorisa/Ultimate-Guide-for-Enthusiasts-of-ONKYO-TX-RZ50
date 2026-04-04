.PHONY: help test lint lint-fix docs docs-serve docker-build docker-run clean

help:
	@echo "Available commands:"
	@echo "  make test       - Run pytest"
	@echo "  make lint       - Run ruff check"
	@echo "  make lint-fix   - Run ruff with auto-fix + black format"
	@echo "  make docs       - Build Sphinx documentation"
	@echo "  make docs-serve - Start Sphinx autobuild server"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run  - Run Docker container"
	@echo "  make clean      - Remove build artifacts"

test:
	cd scripts && python -m pytest tests/ -v --tb=short

lint:
	ruff check scripts/ --exclude scripts/tests/

lint-fix:
	ruff check scripts/ --exclude scripts/tests/ --fix
	black scripts/ --exclude scripts/tests/

docs:
	sphinx-build -b html docs/source docs/_build/html

docs-serve:
	sphinx-autobuild docs/source docs/_build/html --host 0.0.0.0 --port 8000

docker-build:
	docker compose -f docker/docker-compose.yml build

docker-run:
	docker compose -f docker/docker-compose.yml up -d

clean:
	rm -rf docs/_build/
	rm -rf .pytest_cache/
	rm -rf scripts/__pycache__/
	rm -rf scripts/tests/__pycache__/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
