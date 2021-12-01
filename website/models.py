"""The table list in the database. """
from datetime import datetime as dt

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.sql import func

from . import db


class Note(db.Model):
    """" Dinner idea table. """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_active = db.Column(db.Boolean, default=True)


class Needed(db.Model):
    """ The grocery supply table. """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_active = db.Column(db.Boolean, default=True)


class Tasks(db.Model):
    """ The assigned chore table. """
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Integer, db.ForeignKey("chore.id"))
    date = db.Column(db.DateTime(timezone=True), default=dt.today())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_active = db.Column(db.Boolean, default=True)


class Chore(db.Model):
    """ The master list of available chores. """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100), nullable=False)
    is_weekend = db.Column(db.Boolean, default=True)
    chores = db.relationship("Tasks")


# noinspection PyBroadException
class User(db.Model, UserMixin):
    """The user table. """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    needed = db.relationship("Needed", backref="author", lazy=True)
    notes = db.relationship("Note", backref="author", lazy=True)
    chores = db.relationship("Tasks", backref="owner", lazy=True)
    is_parent = db.Column(db.Boolean, default=False)

    def get_reset_token(self, expires_sec=600):
        """ User deffinition of requesting a securtiy token.
        Args:
            expires_sec: the amount of seconds before the security token is no longer valid. default is 10 minutes.

        Returns:
            A valid security token.
        """
        sizer = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return sizer.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        """ Check to ensure the security token is valid and not expired.
        Args:
            token: the security token sent to the user via email.

        Raises:
            raises an exception if token is invalid.
        """
        sizer = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = sizer.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    @staticmethod
    def __repl__():
        """ String repersentation of the User objects. """
        return f"User({'User.first_name', 'User.email'})"
