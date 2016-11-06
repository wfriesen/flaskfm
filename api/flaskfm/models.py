from datetime import datetime
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from humanize import naturaldate

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

    def json(self):
        return {
            'url': url_for('scrobble', scrobble_id=self.id),
            'scrobble_timestamp': self.scrobble_timestamp,
            'artist': self.artist.json(),
            'album': self.album.json(),
            'track': self.track.json()
        }


class Base():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def json(self, url_handler, **kwargs):
        return {
            'url': url_for(url_handler, **kwargs),
            'name': self.name,
            'first_scrobble': naturaldate(min(
                scrobble.scrobble_timestamp for scrobble in self.scrobbles
            )),
            'scrobbles': len(self.scrobbles)
        }


class Artists(db.Model, Base):

    def __init__(self, name):
        super(Artists, self).__init__(self, name)

    def json(self):
        return super(Artists, self).json('artist', artist_id=self.id)


class Albums(db.Model, Base):
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))

    artist = db.relationship('Artists', backref='albums')

    def __init__(self, name, artist):
        super(Albums, self).__init__(self, name)
        self.artist = artist

    def json(self):
        return super(Albums, self).json('album', album_id=self.id)


class Tracks(db.Model, Base):
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))

    artist = db.relationship('Artists', backref='tracks')
    album = db.relationship('Albums', backref='tracks')

    def __init__(self, name, artist, album):
        super(Tracks, self).__init__(self, name)
        self.artist = artist
        self.album = album

    def json(self):
        return super(Tracks, self).json('track', track_id=self.id)
