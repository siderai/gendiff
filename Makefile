install:
	poetry install

package-install:
	poetry install
	poetry build
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 gendiff

diff:
	python gendiff/gendiff.py

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=gendiff --cov-report xml tests/

test-cov-dev:
	poetry run pytest --cov=gendiff

