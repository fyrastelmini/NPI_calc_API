install:
	pip install --upgrade pip &&\
		pip install pytest &&\
			pip install -r calculator_app/requirements.txt
test:
	python -m pytest -vv

format:
	black *.py

lint:
	pylint --disable=R,C */*.py

all: install format lint test