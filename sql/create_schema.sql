CREATE TABLE scrobbles (
  id SERIAL PRIMARY KEY
, artist TEXT
, album TEXT
, track TEXT
, scrobble_timestamp TIMESTAMPTZ
);

COPY scrobbles(artist, album, track, scrobble_timestamp) FROM '/dataimport/scrobbles.csv' DELIMITER ',' CSV;
