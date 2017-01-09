FROM python:2.7
RUN apt-get update && apt-get install --no-install-recommends -y \
    aubio-tools \
    libtag1-dev && \
  apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
  pip install pytaglib
RUN mkdir -p /code /volume/output /volume/files
ADD ./process.py /code
WORKDIR /code
ENTRYPOINT python /code/process.py
