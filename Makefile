lint:
	flake8 .
	mypy .

test:
	pytest -x -s --cov=.
