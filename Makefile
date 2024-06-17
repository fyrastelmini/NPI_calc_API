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

run:
	uvicorn calculator_app.calculator_app:app --reload

all: install lint format test