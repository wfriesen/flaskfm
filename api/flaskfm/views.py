from flask import abort, jsonify, make_response, request
from humanize import naturaldate
from flask_sqlalchemy import sqlalchemy

from models import db, Scrobbles, Artists, Albums, Tracks
from flaskfm import app


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request data'}), 400)


@app.route('/api/v0.1/user_stats', methods=['GET'])
def user_stats():
    last_ten_scrobbles = Scrobbles.query.order_by(
        Scrobbles.scrobble_timestamp.desc()
    ).limit(10)
    scrobble_count, first_scrobble, last_scrobble = db.session.query(
        sqlalchemy.func.count(Scrobbles.id),
        sqlalchemy.func.min(Scrobbles.scrobble_timestamp),
        sqlalchemy.func.max(Scrobbles.scrobble_timestamp)
    ).one()

    return jsonify({
        'stats': {
            'scrobble_count': scrobble_count,
            'first_scrobble': naturaldate(first_scrobble),
            'last_scrobble': last_scrobble,
            'last_ten_scrobbles': [
                scrobble.json() for scrobble in last_ten_scrobbles
            ]
        }
    })


@app.route('/api/v0.1/artist/<int:artist_id>', methods=['GET'])
def artist(artist_id):
    artist = Artists.query.get(artist_id)
    artist_json = artist.json()
    artist_json['albums'] = [album.json() for album in artist.albums]
    return jsonify({'artist': artist_json})


@app.route('/api/v0.1/album/<int:album_id>', methods=['GET'])
def album(album_id):
    album = Albums.query.get(album_id)
    album_json = album.json()
    album_json['tracks'] = [track.json() for track in album.tracks]
    album_json['artist'] = album.artist.json()
    return jsonify({'album': album_json})


@app.route('/api/v0.1/track/<int:track_id>', methods=['GET'])
def track(track_id):
    track = Tracks.query.get(track_id)
    track_json = track.json()
    track_json['album'] = track.album.json()
    track_json['artist'] = track.artist.json()
    return jsonify({'track': track_json})


@app.route('/api/v0.1/scrobble', methods=['POST'])
def create_scrobble():
    if (
        not request.json or
        'artist' not in request.json or
        'album' not in request.json or
        'track' not in request.json
    ):
        abort(400)

    artist = Artists.query.filter_by(name=request.json['artist']).first()
    if artist is None:
        artist = Artists(name=request.json['artist'])

    album = Albums.query.filter_by(name=request.json['album']).first()
    if album is None:
        album = Albums(name=request.json['album'], artist=artist)

    track = Tracks.query.filter_by(name=request.json['track']).first()
    if track is None:
        track = Tracks(name=request.json['track'], artist=artist, album=album)

    new_scrobble = Scrobbles(artist=artist, album=album, track=track)

    db.session.add(new_scrobble)
    db.session.commit()
    return jsonify({
        'success': {
            'message': 'Created new scrobble %s' % new_scrobble.id
        }
    })


@app.route('/api/v0.1/scrobble/<int:scrobble_id>', methods=['DELETE'])
def scrobble(scrobble_id):
    scrobble = Scrobbles.query.filter_by(id=scrobble_id)
    scrobble.delete()
    db.session.commit()
    return jsonify({
        'success': {
            'message': 'Deleted scrobble'
        }
    })


@app.route('/api/v0.1/last_scrobble', methods=['GET'])
def last_scrobble():
    last_scrobble = db.session.query(
        sqlalchemy.func.max(Scrobbles.scrobble_timestamp)
    ).scalar()
    return jsonify({'last_scrobble': last_scrobble})
