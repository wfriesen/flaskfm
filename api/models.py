from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Scrobble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Text)
    album = db.Column(db.Text)
    track = db.Column(db.Text)
    scrobble_timestamp = db.Column(db.DateTime(timezone=True))
