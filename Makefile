build:
	pipenv install --dev

docker:
	docker build -t eu.gcr.io/ssdc-rm-ci/rm/ssdc-rm-toolbox .

flake:
	pipenv run flake8

check:
	PIPENV_PYUP_API_KEY="" pipenv check -i 39611 -i 39608 -i 40014
