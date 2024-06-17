install:
	pip install --upgrade pip &&\
		pip install pytest &&\
			pip install -r calculator_app/requirements.txt
test:
	cd calculator_app &&\
	python -m pytest -vv
test_no_ui:
	cd calculator_app_no_ui &&\
	python -m pytest -vv

format:
	black */*.py

lint:
	pylint --disable=R,C */*.py

run:
	docker-compose up

compose:
	docker-compose up -d		

all: install lint format test test_no_ui