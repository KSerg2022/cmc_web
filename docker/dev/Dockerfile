FROM python:3.10


RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y wkhtmltopdf && apt-get install -y xvfb

RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list \
    && apt-get update && apt-get install -y --no-install-recommends firefox

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /cmc_pr
COPY ../../requirements.txt /cmc_pr
RUN pip install -r /cmc_pr/requirements.txt

COPY ../.. /cmc_pr


#RUN adduser --disabled-password cmc-user
#
#USER cmc-user
