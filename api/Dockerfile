FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD . /code
WORKDIR /code
RUN pip install --upgrade -r requirements.txt
EXPOSE 5000
