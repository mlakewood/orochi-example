.PHONY: test install fmt upload ci

VENV = venv

install: $(VENV)
	. venv/bin/activate; pip install -r requirements.txt

venv:
	virtualenv venv

test:
	. venv/bin/activate; python -m unittest discover src/orochi_example
