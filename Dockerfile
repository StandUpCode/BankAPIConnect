# pull official base image
FROM python:3.8.1-alpine

# set work directory
WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /src/requirements.txt

# install dependencies
RUN apk add --no-cache python3 py3-pip curl bash \
    gcc musl-dev autoconf libffi-dev gmp-dev \
    libxml2 libxslt-dev jpeg-dev zlib-dev \
    build-base python3-dev linux-headers

RUN apk add zbar-dev --update-cache --repository \
    http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /src/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /src/