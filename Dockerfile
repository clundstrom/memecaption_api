FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev python3-venv

# Copy req file
COPY req.txt /

RUN pip3 install -r req.txt
RUN pip3 install uwsgi

RUN useradd -ms /bin/bash uwsgi
USER uwsgi

COPY . /api
WORKDIR /api

