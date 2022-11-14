FROM python:3.8-alpine
MAINTAINER Felipe Sa
ENV PYTHONUNBEFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt


WORKDIR /api_service
COPY ./api_service /api_service

RUN adduser -D felipe
USER felipe