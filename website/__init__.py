from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_admin import Admin
from flask_login import LoginManager
from website.admin import MyView, MyAdminIndexView
from flask_mail import Mail

db = SQLAlchemy()
admin = Admin()
mail = Mail()
DB_NAME = 'database.db'
app = Flask(__name__)


def create_app():
    app.config['SECRET_KEY'] = 'fdsajfhsdk;f jdskfj;a;j'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_Port'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = '12354.e.place@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Vzg6rtbYB880'
    db.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())
    mail.init_app(app)

    from chores.routes import chores
    from ideas.routes import ideas
    from main.routes import main
    from users.routes import users
    from supplies.routes import supply

    app.register_blueprint(chores, url_prefix='/')
    app.register_blueprint(ideas, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(supply, url_prefix='/')

    from .models import User, Note, Chore, Needed

    admin.add_views(MyView(User, db.session), MyView(Note, db.session),
                    MyView(Chore, db.session), MyView(Needed, db.session))
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Authorized Access Only'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
