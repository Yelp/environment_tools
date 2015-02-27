.PHONY: all production docs test tests coverage clean

all: production

production:
	@true

docs:
	tox -e docs

test:
	tox

tests: test
coverage: test

clean:
	rm -rf docs/build/*
	rm -rf environment_tools.egg-info/
	rm -rf .coverage
	rm -rf .tox
	rm -rf virtualenv_run
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

super-clean:
	git clean -ffdx
