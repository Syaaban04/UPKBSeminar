from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mail import Mail
import base64

def base64_encode(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    else:
        return None

db = SQLAlchemy()
mail = Mail()  # Create the Mail object
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.secret_key = 'upkb'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'nursyabanah174@gmail.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = 'zyjg xmnh hpwu eien'  # Replace with your app password

    db.init_app(app)
    mail.init_app(app)  # Initialize the Mail object

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.jinja_env.filters['b64encode'] = base64_encode
    
    from . import models

    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()