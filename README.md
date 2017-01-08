# FlaskFM

A last.fm clone using [Flask](http://flask.pocoo.org/)

## Usage
- Use [Last.fm to csv](https://benjaminbenben.com/lastfm-to-csv/) to get a CSV of your (or any users) scrobbles and save it as `db/scrobbles.csv`.
- Analyze some audio files that you have scrobbled. From within the `scripts` directory:
  - Build the docker image with `docker build -t audioscripts .`
  - Run the actual processing with `docker run -v CODE_DIRECTORY/flaskfm/scripts/output:/volume/output -v MUSIC_DIRECTORY:/volume/files -it audioscripts`, replacing `CODE_DIRECTORY` with wherever you have cloned this repository, and `MUSIC_DIRECTORY` with the location of some (properly tagged) .mp3 and/or .flac files. These must be absolute paths.
- Run `docker-compose up`

## Thanks
FlaskFM makes use of the following projects (among others):
- [Flask](http://flask.pocoo.org/)
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/)
- [wait-for-it](https://github.com/vishnubob/wait-for-it)
- [aubio](https://aubio.org/)
