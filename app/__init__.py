import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='H1R9Qd7QM3^jxz3YfwY'
)
# basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app.models import User, Post, Category
from app import routes
