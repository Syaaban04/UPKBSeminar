from . import db 
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    reset_token = db.Column(db.String(100), nullable=True)  # Token for password reset

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer("your_secret_key")  # Use app's secret key
    return serializer.dumps(email, salt='reset-password')

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    image1 = db.Column(db.LargeBinary)
    image2 = db.Column(db.LargeBinary)
    image3 = db.Column(db.LargeBinary)

class Seminar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    negeri = db.Column(db.String(150))
    daerah = db.Column(db.String(150))
    desc = db.Column(db.Text, nullable = True)
    rating = db.Column(db.Integer)
    image = db.Column(db.LargeBinary)
    price = db.Column(db.String(150))
    location = db.Column(db.String(150))
    facility = db.Column(db.Text, nullable = True)
    capacity = db.Column(db.Integer)
    contact = db.Column(db.String(15))
    link = db.Column(db.String(150))
    image2 = db.Column(db.LargeBinary)
    image3 = db.Column(db.LargeBinary)
    image4 = db.Column(db.LargeBinary)
    google = db.Column(db.String(150))



class Tempat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    negeri = db.Column(db.String(150))
    daerah = db.Column(db.String(150))

