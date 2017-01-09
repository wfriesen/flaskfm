FROM python:2.7.13-alpine
ENV PYTHONUNBUFFERED 1
ADD ./src /code
WORKDIR /code
RUN apk add --no-cache \
    bash \
    postgresql-dev \
  && apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
  && pip install --upgrade -r flaskfm/requirements.txt \
  && apk del .build-deps
EXPOSE 5000
