import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from app import app

basedir = os.path.abspath(os.path.dirname(__file__))


app.config['SQLALCHEMY DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY TRACK MODIFICATIONS'] = False

db = SQLAlchemy(app)



#modele
class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref = db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repre__(self):
        return '<Category%r>' % self.name
