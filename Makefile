install:
	pipenv install --dev

docker:
	docker build -t eu.gcr.io/ssdc-rm-ci/rm/ssdc-rm-toolbox .

flake:
	pipenv run flake8

check:
	pipenv check

unit-test:
	pipenv run pytest --cov-report term-missing --cov . --capture no

test: flake check unit-test
