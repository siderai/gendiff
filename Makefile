install:
	poetry install

lint:
	poetry run flake8 gendiff

diff:
	python gendiff/gendiff.py

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov
