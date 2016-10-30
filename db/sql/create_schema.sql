CREATE TABLE scrobble (
  id SERIAL PRIMARY KEY
, artist TEXT NOT NULL
, album TEXT
, track TEXT NOT NULL
, scrobble_timestamp TIMESTAMPTZ NOT NULL
);

COPY scrobble(artist, album, track, scrobble_timestamp) FROM '/dataimport/scrobbles.csv' DELIMITER ',' CSV;

CREATE VIEW artist_plays_per_year AS
WITH artist_plays_per_year AS (
  SELECT
    CAST(TO_CHAR(s.scrobble_timestamp, 'YYYY') AS INTEGER) y
  , artist
  , COUNT(*) play_count
  , ROW_NUMBER() OVER (
      PARTITION BY CAST(TO_CHAR(s.scrobble_timestamp, 'YYYY') AS INTEGER)
      ORDER BY COUNT(*) DESC
    ) play_rank
  FROM scrobble s
  GROUP BY
    y
  , artist
  ORDER BY
    y DESC
  , play_rank DESC
)
SELECT
  y AS "year"
, artist
, play_count
, play_rank
FROM artist_plays_per_year
WHERE play_rank <= 10
ORDER BY
  y DESC
, play_rank;
