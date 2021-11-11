from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_active = db.Column(db.Boolean, default=True)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Integer, db.ForeignKey('chore.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_active = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)


class Chore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100), nullable=False)
    is_weekend = db.Column(db.Boolean, default=True)
    chores = db.relationship('Tasks')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    notes = db.relationship('Note', backref='author', lazy=True)
    chores = db.relationship('Tasks')
    is_parent = db.Column(db.Boolean, default=False)
