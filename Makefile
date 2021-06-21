build:
	pipenv install --dev

lint:
	pipenv run flake8 . ./sample_loader/tests
	pipenv check

test: lint
	pipenv run pytest --cov-report term-missing --cov . --capture no

docker: test
	docker build -t eu.gcr.io/ssdc-rm-ci/rm/ssdc-rm-toolbox .
