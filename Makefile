lint:
	flake8 .
	mypy .

fmt:
	isort .
	black .

test:
	pytest -x -s --cov=.
