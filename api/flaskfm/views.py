from datetime import datetime
from flask import abort, jsonify, make_response, request
from humanize import naturaldate, naturaltime
from psycopg2 import tz
from flask_sqlalchemy import sqlalchemy

from crossdomain import crossdomain
from models import db, Scrobbles, Artists, Albums, Tracks
from flaskfm import app


def get_last_scrobble_timestamp():
    last_scrobble_timestamp = db.session.query(
        sqlalchemy.func.max(Scrobbles.scrobble_timestamp)
    ).scalar()
    return last_scrobble_timestamp


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request data'}), 400)


@app.route('/flaskfm/api/v0.1/user_stats', methods=['GET'])
@crossdomain(origin='*')
def user_stats():
    scrobble_count = Scrobbles.query.count()
    first_scrobble = db.session.query(
        sqlalchemy.func.min(Scrobbles.scrobble_timestamp)
    ).scalar()
    last_scrobble = get_last_scrobble_timestamp()
    return jsonify(
        {
            'stats': {
                'scrobble_count': scrobble_count,
                'first_scrobble': naturaldate(first_scrobble),
                'last_scrobble': last_scrobble
            }
        }
    )


@app.route('/flaskfm/api/v0.1/last_scrobble', methods=['GET'])
@crossdomain(origin='*')
def last_scrobble():
    last_scrobble = get_last_scrobble_timestamp()
    return jsonify({'last_scrobble': last_scrobble})


@app.route('/flaskfm/api/v0.1/create_new_scrobble', methods=['POST'])
@crossdomain(origin='*')
def create_new_scrobble():
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
        track = Tracks(name=request.json['track'], artist=artist, track=track)

    new_scrobble = Scrobbles(artist=artist, album=album, track=track)

    db.session.add(new_scrobble)
    db.session.commit()
    return jsonify({
        'success': {
            'message': 'Created new scrobble %s' % new_scrobble.id
        }
    })


@app.route(
    '/flaskfm/api/v0.1/delete_scrobble/<int:id>',
    methods=['DELETE', 'OPTIONS']
)
@crossdomain(origin='*')
def delete_scrobble(id):
    if request.method == 'OPTIONS':
        return jsonify({'response': 'All good'})
    scrobble = Scrobbles.query.filter_by(id=id)
    if scrobble.count() == 0:
        return jsonify({'errors': {'message': 'Scrobbles does not exist'}})

    scrobble.delete()
    db.session.commit()
    return jsonify({'success': {'message': 'Deleted scrobble ID: %d' % (id)}})


@app.route('/flaskfm/api/v0.1/recent', methods=['GET'])
@crossdomain(origin='*')
def recent_scrobbles():
    now = datetime.now(tz=tz.FixedOffsetTimezone(offset=0, name=None))
    scrobbles = Scrobbles.query.order_by(
        Scrobbles.scrobble_timestamp.desc()
    ).limit(10)
    scrobbles_json = [{
        'id': scrobble.id,
        'artist': scrobble.artist.name,
        'album': scrobble.album.name,
        'track': scrobble.track.name,
        'timestamp': scrobble.scrobble_timestamp,
        'human_timestamp': naturaltime(now - scrobble.scrobble_timestamp)
    } for scrobble in scrobbles]
    return jsonify({'scrobbles': scrobbles_json})


@app.route(
    '/flaskfm/api/v0.1/scrobble_artist_info/<int:scrobble_id>',
    methods=['GET']
)
@crossdomain(origin='*')
def scrobble_artist_info(scrobble_id):
    artist = Scrobbles.query.get(scrobble_id).artist

    first_scrobble = db.session.query(
        sqlalchemy.func.min(Scrobbles.scrobble_timestamp)
    ).filter_by(artist_id=artist.id).scalar()

    last_scrobble_id = db.session.query(
        sqlalchemy.func.max(Scrobbles.id)
    ).filter_by(artist_id=artist.id).scalar()

    return jsonify({
        'scrobble_artist_info': {
            'info': {
                'artist': artist.name,
                'total_scrobbles': len(artist.scrobbles),
                'first_scrobble': naturaldate(first_scrobble)
            },
            'albums': [{
                'album': album.name,
                'play_count': len(album.scrobbles),
                'first_scrobble': naturaldate(first_scrobble),
                'last_scrobble_id': last_scrobble_id
            } for album in artist.albums]
        }
    })


@app.route(
    '/flaskfm/api/v0.1/scrobble_album_info/<int:scrobble_id>',
    methods=['GET']
)
@crossdomain(origin='*')
def scrobble_album_info(scrobble_id):
    album = Scrobbles.query.get(scrobble_id).album
    first_scrobble = db.session.query(
        sqlalchemy.func.min(Scrobbles.scrobble_timestamp)
    ).filter_by(album_id=album.id).scalar()

    album_info = {
        'artist': album.artist.name,
        'album': album.name,
        'total_scrobbles': len(album.scrobbles),
        'first_scrobble': naturaldate(first_scrobble)
    }

    tracks = []
    for track in album.tracks:
        first_scrobble = db.session.query(
            sqlalchemy.func.min(Scrobbles.scrobble_timestamp)
        ).filter_by(track_id=track.id).scalar()
        last_scrobble_id = db.session.query(
            sqlalchemy.func.max(Scrobbles.id)
        ).filter_by(track_id=track.id).scalar()
        tracks.append({
            'track': track.name,
            'play_count': len(track.scrobbles),
            'first_scrobble': naturaldate(first_scrobble),
            'last_scrobble_id': last_scrobble_id
        })

    return jsonify({
        'scrobble_album_info': {
            'album_info': album_info,
            'tracks': tracks
        }
    })


@app.route(
    '/flaskfm/api/v0.1/scrobble_track_info/<int:scrobble_id>',
    methods=['GET']
)
@crossdomain(origin='*')
def scrobble_track_info(scrobble_id):
    track = Scrobbles.query.get(scrobble_id).track
    first_scrobble = db.session.query(
        sqlalchemy.func.min(Scrobbles.scrobble_timestamp)
    ).filter_by(track_id=track.id).scalar()

    track_info = {
        'artist': track.artist.name,
        'album': track.album.name,
        'track': track.name,
        'total_scrobbles': len(track.scrobbles),
        'first_scrobble': naturaldate(first_scrobble)
    }

    return jsonify({'scrobble_track_info': {'track_info': track_info}})
