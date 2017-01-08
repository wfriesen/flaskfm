FROM python:2.7
RUN apt-get update && apt-get install -y \
  aubio-tools \
  libtag1-dev && \
  apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install pytaglib
RUN mkdir -p /code /volume/output /volume/files
ADD ./process.py /code
WORKDIR /code
ENTRYPOINT python /code/process.py
