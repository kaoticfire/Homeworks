from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_admin import Admin
from flask_login import LoginManager
from .admin import MyView, MyAdminIndexView
from flask_mail import Mail

db = SQLAlchemy()
admin = Admin()
DB_NAME = 'database.db'
app = Flask(__name__)
mail = Mail()


def create_app():
    app.config['SECRET_KEY'] = 'fdsajfhsdk;f jdskfj;a;j'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_Port'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = '12354.e.place@gmail.com'
    app.config['MAIL_PASSWORD'] = 'qvmwexnkmkrhnppm'
    db.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())
    mail.init_app(app)

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
