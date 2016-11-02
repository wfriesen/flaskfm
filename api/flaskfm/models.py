from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Scrobbles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'))
    scrobble_timestamp = db.Column(db.DateTime(timezone=True))

    artist = db.relationship('Artists', backref='scrobbles')
    album = db.relationship('Albums', backref='scrobbles')
    track = db.relationship('Tracks', backref='scrobbles')

    def __init__(self, artist, album, track):
        self.artist = artist
        self.album = album
        self.track = track
        self.scrobble_timestamp = datetime.now()


class Artists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name


class Albums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    name = db.Column(db.Text)

    artist = db.relationship('Artists', backref='albums')

    def __init__(self, name, artist):
        self.name = name
        self.artist = artist


class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    name = db.Column(db.Text)

    artist = db.relationship('Artists', backref='tracks')
    album = db.relationship('Albums', backref='tracks')

    def __init__(self, name, artist, album):
        self.name = name
        self.artist = artist
        self.album = album
