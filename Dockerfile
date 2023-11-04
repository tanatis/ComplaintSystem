FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/
#COPY portfolio /app/portfolio
#COPY static_files /app/static_files
#COPY templates /app/templates
#COPY manage.py /app/manage.py
#COPY db.sqlite3 /app/db.sqlite3