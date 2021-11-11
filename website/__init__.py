from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_admin import Admin
from flask_login import LoginManager
from .admin import MyView, MyAdminIndexView

db = SQLAlchemy()
admin = Admin()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fdsajfhsdk;f jdskfj;a;j'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Chore

    admin.add_views(MyView(User, db.session), MyView(Note, db.session), MyView(Chore, db.session))
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Authorized Access Only'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
