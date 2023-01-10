FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=HomeManager.settings
EXPOSE 8000
