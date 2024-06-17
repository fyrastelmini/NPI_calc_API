FROM python:3.8-slim-buster

WORKDIR /calculator_app_no_ui

ADD . /calculator_app_no_ui

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "calculator_app_no_ui:app", "--host", "0.0.0.0", "--port", "5001"]