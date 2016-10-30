#!flaskfm/bin/python
from datetime import datetime
from flask import abort, Flask, jsonify, make_response, request
from humanize import naturaldate, naturaltime
from psycopg2 import tz
from sqlalchemy import func
from sqlalchemy.sql import text

from crossdomain import crossdomain
from models import db, Scrobble
from secrets import database_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db.init_app(app)


def get_last_scrobble_timestamp():
    last_scrobble_timestamp = db.session.query(
        func.max(Scrobble.scrobble_timestamp)
    ).scalar()
    return last_scrobble_timestamp


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request data'}), 400)


@app.route('/flaskfm/api/v0.1/user_stats', methods=['GET'])
@crossdomain(origin='*')
def user_stats():
    scrobble_count = Scrobble.query.count()
    first_scrobble = db.session.query(
        func.min(Scrobble.scrobble_timestamp)
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

    new_scrobble = Scrobble(
        artist=request.json['artist'],
        album=request.json['album'],
        track=request.json['track']
    )

    db.session.add(new_scrobble)
    db.session.commit()
    return jsonify({'last_scrobble': new_scrobble.album})


@app.route(
    '/flaskfm/api/v0.1/delete_scrobble/<int:id>',
    methods=['DELETE', 'OPTIONS']
)
@crossdomain(origin='*')
def delete_scrobble(id):
    if request.method == 'OPTIONS':
        return jsonify({'response': 'All good'})
    scrobble = Scrobble.query.filter_by(id=id)
    if scrobble.count() == 0:
        return jsonify({'errors': {'message': 'Scrobble does not exist'}})

    scrobble.delete()
    db.session.commit()
    return jsonify({'success': {'message': 'Deleted scrobble ID: %d' % (id)}})


@app.route('/flaskfm/api/v0.1/recent', methods=['GET'])
@crossdomain(origin='*')
def recent_scrobbles():
    now = datetime.now(tz=tz.FixedOffsetTimezone(offset=0, name=None))
    scrobbles = Scrobble.query.order_by(
        Scrobble.scrobble_timestamp.desc()
    ).limit(10)
    scrobbles_json = [{
        'id': scrobble.id,
        'artist': scrobble.artist,
        'album': scrobble.album,
        'track': scrobble.track,
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
    s = text("""SELECT
  MIN(a.artist) artist
, MIN(a.scrobble_timestamp) first_scrobble
, COUNT(*) total_scrobbles
FROM scrobble s
JOIN scrobble a
  ON a.artist = s.artist
WHERE s.id = :scrobble_id""")

    results = db.engine.execute(s, scrobble_id=scrobble_id)

    artist_info = [{
        'artist': artist,
        'total_scrobbles': total_scrobbles,
        'first_scrobble': naturaldate(first_scrobble)
    } for (artist, first_scrobble, total_scrobbles) in results]

    s = text("""
SELECT
  a.album
, COUNT(*) play_count
, MIN(a.scrobble_timestamp) first_scrobble
FROM scrobble s
JOIN scrobble a
  ON a.artist = s.artist
  AND a.album IS NOT NULL
WHERE s.id = :scrobble_id
GROUP BY
  a.album
ORDER BY
  play_count DESC
""")

    results = db.engine.execute(s, scrobble_id=scrobble_id)

    albums = [{
        'album': album,
        'play_count': play_count,
        'first_scrobble': naturaldate(first_scrobble)
    } for (album, play_count, first_scrobble) in results]

    return jsonify({
        'scrobble_artist_info': {
            'info': artist_info[0],
            'albums': albums
        }
    })


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
