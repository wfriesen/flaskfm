CREATE TABLE sample_data (
  artist TEXT NOT NULL
, album TEXT
, track TEXT NOT NULL
, scrobble_timestamp TIMESTAMPTZ NOT NULL
);

CREATE TABLE files (
  id INTEGER PRIMARY KEY NOT NULL
, name TEXT NOT NULL
, artist_name TEXT NOT NULL
, album_name TEXT NOT NULL
, track_name TEXT NOT NULL
);

CREATE TABLE onsets (
  file_id INTEGER REFERENCES files(id)
, onset NUMERIC
);

CREATE TABLE pitch (
  file_id INTEGER REFERENCES files(id)
, time NUMERIC
, pitch NUMERIC
);

COPY sample_data(artist, album, track, scrobble_timestamp) FROM '/audio_data/scrobbles.csv' DELIMITER ',' CSV;

COPY files(id, name, artist_name, album_name, track_name) FROM '/audio_data/files.csv' DELIMITER ',' CSV;

COPY onsets(file_id, onset) FROM '/audio_data/onsets.csv' DELIMITER ',' CSV;

DO $$DECLARE
  file RECORD;
  partition_name TEXT;
BEGIN

  FOR file IN (
    SELECT
      id
    FROM files
    GROUP BY
      id
  )
  LOOP

    partition_name := 'pitch_' || file.id;
    EXECUTE 'CREATE TABLE ' || partition_name || ' (check (file_id = ' || file.id || ')) INHERITS (pitch);';

  END LOOP;

END
$$;

CREATE OR REPLACE FUNCTION pitch_insert()
RETURNS TRIGGER AS $$
BEGIN
  EXECUTE 'INSERT INTO pitch_' || NEW.file_id || '(file_id, time, pitch) VALUES (' || NEW.file_id || ', ' || NEW.time || ', ' || NEW.pitch || ');';
  RETURN NULL;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER trg_pitch_insert
  BEFORE INSERT ON pitch
  FOR EACH ROW EXECUTE PROCEDURE pitch_insert();

COPY pitch(file_id, time, pitch) FROM '/audio_data/pitch.csv' DELIMITER ',' CSV;

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
