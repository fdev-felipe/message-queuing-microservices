FROM python:3.8-alpine
MAINTAINER Felipe Sa
ENV PYTHONUNBEFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

WORKDIR /stock_service
COPY ./stock_service /stock_service

RUN adduser -D felipe
USER felipe