lint:
	flake8 .
	mypy .

test:
	pytest tests/
