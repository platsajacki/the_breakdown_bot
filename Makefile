lint:
	flake8 .
	mypy .

test:
	pytest --cov=.
