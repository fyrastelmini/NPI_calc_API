install:
	pip install --upgrade pip &&\
		pip install pytest &&\
			pip install -r calculator_app/requirements.txt
test:
	cd calculator_app &&\
	python -m pytest -vv

format:
	black calculator_app/*.py

lint:
	pylint --disable=R,C */*.py

run:
	docker-compose up
		

all: install lint format test