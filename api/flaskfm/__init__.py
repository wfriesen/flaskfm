from flask import Flask
import os

from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

pg_username = os.environ['POSTGRES_USER']
pg_password = os.environ['POSTGRES_PASSWORD']
pg_db = os.environ['POSTGRES_DB']
database_uri = 'postgresql://%s:%s@db/%s' % (pg_username, pg_password, pg_db)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db.init_app(app)

from flaskfm import views
