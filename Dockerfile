FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /django-project

COPY requirements/local.txt requirements/local.txt

COPY . .

RUN pip3 install -r requirements/local.txt
RUN python3 manage.py migrate