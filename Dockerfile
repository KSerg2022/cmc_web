FROM python:3.10
#FROM python:3.10-alpine3.17

RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y wkhtmltopdf && apt-get install -y xvfb

RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends firefox

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#COPY requirements.txt /cmc/requirements.txt
COPY . /cmc
WORKDIR /cmc

EXPOSE 8000

RUN pip install -r /cmc/requirements.txt

RUN adduser --disabled-password cmc-user

USER cmc-user
