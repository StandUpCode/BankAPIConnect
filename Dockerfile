# Name the single Python image we're using everywhere.
ARG python=python:alpine3.15

# Build stage:
FROM ${python} AS compile-image
# pull official base image




RUN apk add   --no-cache python3 py3-pip curl bash \
    gcc musl-dev autoconf libffi-dev gmp-dev cmake \
    libxml2 libxslt-dev jpeg-dev zlib-dev \
    build-base python3-dev linux-headers

RUN apk add zbar-dev --update-cache --repository \
     http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted

RUN set -eux

RUN apk add --no-cache --virtual .build-deps build-base \
    libressl-dev libffi-dev gcc g++ musl-dev python3-dev 

# Create the virtual environment.
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH


# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /src/requirements.txt

# install dependencies

RUN pip install --upgrade pip setuptools wheel

RUN pip install -r /src/requirements.txt


FROM ${python}


COPY --from=compile-image /venv /venv

ENV PATH=/venv/bin:$PATH

# copy project

COPY . /app/


EXPOSE 8080

CMD sleep 10
