# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /service-code
COPY requirements.txt /service-code/
RUN pip install -r requirements.txt
COPY . /service-code/

