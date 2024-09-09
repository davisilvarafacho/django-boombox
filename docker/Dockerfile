FROM python:3.10

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py collectstatic