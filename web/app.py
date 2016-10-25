#!flaskfm/bin/python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from secrets import database_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(app)


class Scrobble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(1000))
    album = db.Column(db.String(1000))
    track = db.Column(db.String(1000))
    scrobble_timestamp = db.Column(db.DateTime(timezone=True))

    def __init__(self, artist, album, track, scrobble_timestamp):
        self.artist = artist
        self.album = album
        self.track = track
        self.scrobble_timestamp = scrobble_timestamp


@app.route('/flaskfm/api/v0.1/recent', methods=['GET'])
def recent_scrobbles():
    scrobbles = Scrobble.query.order_by(
        Scrobble.scrobble_timestamp.desc()
    ).limit(10)
    scrobbles_json = [{
        'artist': scrobble.artist,
        'album': scrobble.album,
        'track': scrobble.track,
        'timestamp': scrobble.scrobble_timestamp
    } for scrobble in scrobbles]
    return jsonify({'scrobbles': scrobbles_json})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
