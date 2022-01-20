""" Main configuration of the application """

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_admin import Admin
from flask_login import LoginManager
from website.admin import MyView, MyAdminIndexView
from flask_mail import Mail
from website.config import Config
from datetime import timedelta

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin()
mail = Mail()


def create_app(config_class=Config):
    """ create, configure, and start application """
    app = Flask(__name__)
    app.config.from_object(Config)
    app.permanent_session_lifetime = timedelta(minutes=5)

    db.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())
    mail.init_app(app)

    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Authorized Access Only'
    login_manager.login_message_category = 'info'
    login_manager.refresh_view = 'users.login'
    login_manager.needs_refresh_message = 'Session timeout, please re-login to continue'
    login_manager.needs_refresh_message_category = 'info'
    login_manager.init_app(app)

    from website.chores.routes import chores
    from website.ideas.routes import ideas
    from website.users.routes import users
    from website.supplies.routes import supply
    from website.errors.handlers import errors
    from website.messages.routes import messages

    app.register_blueprint(chores, url_prefix='/')
    app.register_blueprint(ideas, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(supply, url_prefix='/')
    app.register_blueprint(errors, url_prefix='/')
    app.register_blueprint(messages, url_prefix='/')

    from .models import User, Note, Chore, Needed, Tasks, Message

    admin.add_views(MyView(User, db.session), MyView(Note, db.session),
                    MyView(Chore, db.session), MyView(Needed, db.session),
                    MyView(Tasks, db.session), MyView(Message, db.session))
    create_database(app)
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        """ look for user id for startup / login """
        return User.query.get(int(user_id))
    return app


def create_database(app):
    """ Create the database as needed """
    if not path.exists(Config.SQLALCHEMY_DATABASE_URI):
        db.create_all(app=app)
