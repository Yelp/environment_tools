.PHONY: all production docs test tests coverage clean

BIND_FILES ?= undefined

all: production

production:
	@true

docs:
	tox -e docs

test:
	tox

tests: test
coverage: test

mapping:
ifeq ("$(BIND_FILES)","undefined")
	$(error BIND_FILES is not set. BIND_FILES must point to a bind checkout containing local zones)
endif
	tox -e mapping $(BIND_FILES) environment_tools/data/location_mapping.json


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
