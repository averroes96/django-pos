FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements/local.txt requirements/local.txt
COPY . .

RUN pip3 install -r requirements/local.txt
RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]