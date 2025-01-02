from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
import base64

def base64_encode(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    else:
        return None

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'upkb'

    # Database configuration
    # Check for a DATABASE_URL environment variable (used in deployment) or default to SQLite for local development
    database_url = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    
    # Render PostgreSQL databases use URLs with SSL; update the URI if necessary
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'nursyabanah174@gmail.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = 'zyjg xmnh hpwu eien'  # Replace with your app password

    db.init_app(app)
    mail.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.jinja_env.filters['b64encode'] = base64_encode

    with app.app_context():
        db.create_all()  # Ensure tables are created

    return app
