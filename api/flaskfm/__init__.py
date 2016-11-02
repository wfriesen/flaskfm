from flask import Flask
from secrets import database_uri
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db.init_app(app)


from flaskfm import views
