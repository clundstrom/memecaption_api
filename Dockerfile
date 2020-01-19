FROM ubuntu:18.04

MAINTAINER Chris Lundstrom "contact@clundstrom.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev


WORKDIR /app

COPY . /app

# We copy just the requirements.txt first to leverage Docker cache
COPY ./req.txt /app/req.txt
RUN pip install -r req.txt

RUN pip install flask
RUN pip install flask_sqlalchemy

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]