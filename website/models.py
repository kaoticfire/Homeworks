from . import db, app
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_active = db.Column(db.Boolean, default=True)


class Needed(db.Model):
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
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)


class Chore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100), nullable=False)
    is_weekend = db.Column(db.Boolean, default=True)
    chores = db.relationship('Tasks')


# noinspection PyBroadException
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    needed = db.relationship('Needed', backref='author', lazy=True)
    notes = db.relationship('Note', backref='author', lazy=True)
    chores = db.relationship('Tasks', backref='owner', lazy=True)
    is_parent = db.Column(db.Boolean, default=False)

    def get_reset_token(self, expires_sec=600):
        sizer = Serializer(app.config['SECRET_KEY'], expires_sec)
        return sizer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        sizer = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = sizer.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @staticmethod
    def __repl__():
        return f"User({'User.first_name', 'User.email'})"
