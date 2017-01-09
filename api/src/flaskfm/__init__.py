from flask import Flask
from flask_sqlalchemy import sqlalchemy
import os

from models import db, Scrobbles

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

pg_username = os.environ['POSTGRES_USER']
pg_password = os.environ['POSTGRES_PASSWORD']
pg_db = os.environ['POSTGRES_DB']
database_uri = 'postgresql://%s:%s@db/%s' % (pg_username, pg_password, pg_db)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db.init_app(app)

from flaskfm import views


with app.app_context():
    db.create_all()
    if Scrobbles.query.first() is None:
        print('Importing sample data')
        s = sqlalchemy.text("""SELECT import_sample_data();""")
        db.session.execute(s)
        db.session.commit()
