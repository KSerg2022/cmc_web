FROM python:3.10
#FROM python:3.10-alpine3.17

RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y wkhtmltopdf && apt-get install -y xvfb

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#COPY requirements.txt /cmc/requirements.txt
COPY . /cmc
WORKDIR /cmc

EXPOSE 8000

RUN pip install -r /cmc/requirements.txt

RUN adduser --disabled-password cmc-user

USER cmc-user
