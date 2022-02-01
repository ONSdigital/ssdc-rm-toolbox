install:
	pipenv install --dev

docker:
	docker build -t europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-toolbox .

flake:
	pipenv run flake8

check:
	pipenv check

unit-test:
	pipenv run pytest --cov-report term-missing --cov . --capture no

test: flake check unit-test
