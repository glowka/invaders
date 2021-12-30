lint:
	isort --check-only --atomic . || ERROR=1; black --check . || ERROR=1; exit $${ERROR}

format:
	black .
	isort --atomic .

test:
	pytest


run-sample:
	python run_sample.py
