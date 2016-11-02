CREATE TABLE scrobble_csv (
  artist TEXT NOT NULL
, album TEXT
, track TEXT NOT NULL
, scrobble_timestamp TIMESTAMPTZ NOT NULL
);

COPY scrobble_csv(artist, album, track, scrobble_timestamp) FROM '/dataimport/scrobbles.csv' DELIMITER ',' CSV;

CREATE TABLE artists (
  id SERIAL PRIMARY KEY
, name TEXT NOT NULL UNIQUE
);

INSERT INTO artists (name)
SELECT
  artist
FROM scrobble_csv
GROUP BY
  artist;

CREATE TABLE albums (
  id SERIAL PRIMARY KEY
, artist_id INTEGER REFERENCES artists (id)
, name TEXT NOT NULL
);

INSERT INTO albums (
  artist_id
, name
)
SELECT
  a.id
, sc.album
FROM scrobble_csv sc
JOIN artists a
  ON a.name = sc.artist
WHERE sc.album IS NOT NULL
GROUP BY
  a.id
, sc.album;

CREATE TABLE tracks (
  id SERIAL PRIMARY KEY
, artist_id INTEGER REFERENCES artists(id)
, album_id INTEGER REFERENCES albums(id)
, name TEXT NOT NULL
);

INSERT INTO tracks (
  artist_id
, album_id
, name
)
SELECT
  a.id artist_id
, albums.id album_id
, sc.track
FROM scrobble_csv sc
JOIN artists a
  ON a.name = sc.artist
JOIN albums
  ON albums.name = sc.album
GROUP BY
  a.id
, albums.id
, sc.track;

CREATE TABLE scrobbles (
  id SERIAL PRIMARY KEY
, artist_id INTEGER REFERENCES artists (id)
, album_id INTEGER REFERENCES albums (id)
, track_id INTEGER REFERENCES tracks (id)
, scrobble_timestamp TIMESTAMPTZ NOT NULL
);

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
FROM scrobble_csv sc
JOIN artists a
  ON a.name = sc.artist
JOIN albums
  ON albums.artist_id = a.id
  AND albums.name = sc.album
JOIN tracks t
  ON t.artist_id = a.id
  AND t.album_id = albums.id
  AND t.name = sc.track;

DROP TABLE scrobble_csv;



-- CREATE VIEW artist_plays_per_year AS
-- WITH artist_plays_per_year AS (
--   SELECT
--     CAST(TO_CHAR(s.scrobble_timestamp, 'YYYY') AS INTEGER) y
--   , artist
--   , COUNT(*) play_count
--   , ROW_NUMBER() OVER (
--       PARTITION BY CAST(TO_CHAR(s.scrobble_timestamp, 'YYYY') AS INTEGER)
--       ORDER BY COUNT(*) DESC
--     ) play_rank
--   FROM scrobble s
--   GROUP BY
--     y
--   , artist
--   ORDER BY
--     y DESC
--   , play_rank DESC
-- )
-- SELECT
--   y AS "year"
-- , artist
-- , play_count
-- , play_rank
-- FROM artist_plays_per_year
-- WHERE play_rank <= 10
-- ORDER BY
--   y DESC
-- , play_rank;
