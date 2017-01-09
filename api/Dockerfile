FROM python:2.7.13-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD . /code
WORKDIR /code
RUN apk update && \
  apk add --no-cache \
  gcc \
  musl-dev \
  postgresql-dev \
  bash
RUN pip install --upgrade -r flaskfm/requirements.txt
EXPOSE 5000
