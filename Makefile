build:
	pipenv install --dev

lint:
	pipenv run flake8 . ./sample_loader/tests
	pipenv check

test: lint
	pipenv run pytest --cov-report term-missing --cov . --capture no

docker: test
	docker build -t eu.gcr.io/ons-ci-rm/rm/ssdc-rm-toolbox .
