build:
	pipenv install --dev

lint:
	pipenv run flake8 . ./sample_loader/tests
    # TODO reinstate this once https://github.com/pypa/pipenv/issues/4188 is resolved
	#pipenv check

test: lint
	pipenv run pytest --cov-report term-missing --cov . --capture no

docker: test
	docker build -t eu.gcr.io/ssdc-rm-ci/rm/ssdc-rm-toolbox .
