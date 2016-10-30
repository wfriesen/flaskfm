from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Scrobble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Text)
    album = db.Column(db.Text)
    track = db.Column(db.Text)
    scrobble_timestamp = db.Column(db.DateTime(timezone=True))

    def __init__(self, artist, album, track):
        self.artist = artist
        self.album = album
        self.track = track
        self.scrobble_timestamp = datetime.now()
