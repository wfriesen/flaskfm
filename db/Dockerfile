FROM postgres
COPY sql/* /docker-entrypoint-initdb.d/
RUN mkdir /dataimport
COPY ./scrobbles.csv ./audio_data/* /dataimport/
