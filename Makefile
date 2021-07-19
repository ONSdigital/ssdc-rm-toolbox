build:
	pipenv install --dev

docker:
	docker build -t eu.gcr.io/ssdc-rm-ci/rm/ssdc-rm-toolbox .

flake:
	pipenv run flake8

check:
	pipenv check
