.PHONY: install test lint format run clean

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy pytest tests/ -v

lint:
	ruff check .

format:
	ruff format .

run:
	python main.py

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache
	find . -name "*.pyc" -not -path "./.venv/*" -delete
	find . -name "__pycache__" -not -path "./.venv/*" -type d -exec rm -rf {} +
