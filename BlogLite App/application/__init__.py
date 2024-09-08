from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from os.path import join, dirname, realpath
from flask_login import LoginManager

db = SQLAlchemy()
UPLOAD_FOLDER=join(dirname(realpath(__file__)), 'static/uploads/..')
def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config['SECRET_KEY'] = 'Eb98hjj45ghh78lLp245'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloglite.db'
    
    db.init_app(app)
    # registering blueprints in app
    from .controllers import views
    #from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    #app.register_blueprint(auth, url_prefix='/')
    from .models import User,Post,Like,Comment
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    #app.app_context().push()
    return app

def create_database(app):
    if not path.exists("application/bloglite.db"):
        db.create_all(app = app)