CREATE TABLE sample_data (
  artist TEXT NOT NULL
, album TEXT
, track TEXT NOT NULL
, scrobble_timestamp TIMESTAMPTZ NOT NULL
);

COPY sample_data(artist, album, track, scrobble_timestamp) FROM '/dataimport/scrobbles.csv' DELIMITER ',' CSV;

CREATE OR REPLACE FUNCTION import_sample_data()
RETURNS void AS $$
BEGIN

  INSERT INTO artists (name)
  SELECT
    artist
  FROM sample_data
  GROUP BY
    artist;

  INSERT INTO albums (
    artist_id
  , name
  )
  SELECT
    a.id
  , sc.album
  FROM sample_data sc
  JOIN artists a
    ON a.name = sc.artist
  WHERE sc.album IS NOT NULL
  GROUP BY
    a.id
  , sc.album;

  INSERT INTO tracks (
    artist_id
  , album_id
  , name
  )
  SELECT
    a.id artist_id
  , albums.id album_id
  , sc.track
  FROM sample_data sc
  JOIN artists a
    ON a.name = sc.artist
  JOIN albums
    ON albums.name = sc.album
  GROUP BY
    a.id
  , albums.id
  , sc.track;

  INSERT INTO scrobbles (
    artist_id
  , album_id
  , track_id
  , scrobble_timestamp
  )
  SELECT
    a.id artist_id
  , albums.id album_id
  , t.id track_id
  , sc.scrobble_timestamp
  FROM sample_data sc
  JOIN artists a
    ON a.name = sc.artist
  JOIN albums
    ON albums.artist_id = a.id
    AND albums.name = sc.album
  JOIN tracks t
    ON t.artist_id = a.id
    AND t.album_id = albums.id
    AND t.name = sc.track;

END;
$$ LANGUAGE plpgsql;
