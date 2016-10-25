# FlaskFM

A last.fm clone using [Flask](http://flask.pocoo.org/)

## Usage
- Use [Last.fm to csv](https://benjaminbenben.com/lastfm-to-csv/) to get a CSV of your (or any users) scrobbles and save it as `./scrobbles.csv`.
- Run `docker-compose up`

## Development
Follow these steps to run the flask app outside of docker.
- Repoint the database host name: `export POSTGRES_URI=postgresql://docker:docker@localhost/docker`
- Start up the database: `docker-compose up db`
- Run the local server in `./api` with `python app.py`
