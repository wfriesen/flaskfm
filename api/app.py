#!flaskfm/bin/python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from crossdomain import crossdomain
from secrets import database_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(app)


class Scrobble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Text)
    album = db.Column(db.Text)
    track = db.Column(db.Text)
    scrobble_timestamp = db.Column(db.DateTime(timezone=True))


@app.route('/flaskfm/api/v0.1/recent', methods=['GET'])
@crossdomain(origin='*')
def recent_scrobbles():
    scrobbles = Scrobble.query.order_by(
        Scrobble.scrobble_timestamp.desc()
    ).limit(10)
    scrobbles_json = [{
        'id': scrobble.id,
        'artist': scrobble.artist,
        'album': scrobble.album,
        'track': scrobble.track,
        'timestamp': scrobble.scrobble_timestamp
    } for scrobble in scrobbles]
    return jsonify({'scrobbles': scrobbles_json})


@app.route(
    '/flaskfm/api/v0.1/top_artists_per_year/<int:year>',
    methods=['GET']
)
def top_artists_per_year(year):
    s = text("""SELECT
  year
, artist
, play_count
, play_rank
FROM artist_plays_per_year
WHERE year = :year""")

    results = db.engine.execute(s, year=year)

    results_json = [{
        'year': year,
        'artist': artist,
        'play_count': play_count,
        'play_rank': play_rank
    } for (year, artist, play_count, play_rank) in results]
    return jsonify({'top_artists_per_year': results_json})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
