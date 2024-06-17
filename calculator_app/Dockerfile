FROM python:3.8-slim-buster

WORKDIR /calculator_app

ADD . /calculator_app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "calculator_app:app", "--host", "0.0.0.0", "--port", "5000"]