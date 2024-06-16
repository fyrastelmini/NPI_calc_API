install:
	pip install --upgrade pip &&\
		pip install pytest &&\
			pip install -r requirements.txt
test:
	python -m pytest -vv

format:
	black calculator_app/*.py

lint:
	pylint --disable=R,C */*.py

all: install lint format test