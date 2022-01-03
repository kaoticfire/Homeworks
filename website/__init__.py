from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_admin import Admin
from flask_login import LoginManager
from website.admin import MyView, MyAdminIndexView
from flask_mail import Mail
from website.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Authorized Access Only'
admin = Admin()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())
    mail.init_app(app)
    login_manager.init_app(app)

    from website.chores.routes import chores
    from website.ideas.routes import ideas
    from website.users.routes import users
    from website.supplies.routes import supply
    from website.errors.handlers import errors

    app.register_blueprint(chores, url_prefix='/')
    app.register_blueprint(ideas, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(supply, url_prefix='/')
    app.register_blueprint(errors, url_prefix='/')

    from .models import User, Note, Chore, Needed, Tasks

    admin.add_views(MyView(User, db.session), MyView(Note, db.session),
                    MyView(Chore, db.session), MyView(Needed, db.session),
                    MyView(Tasks, db.session))
    create_database(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    return app


def create_database(app):
    if not path.exists(Config.SQLALCHEMY_DATABASE_URI):
        db.create_all(app=app)
