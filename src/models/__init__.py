from src import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    passowrd = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Integer, nullable=True)
    address = db.Column(db.Integer, nullable=True)
    phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    avatar = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(60), default="USER")
    organize = db.Column(db.String(100), nullable=True)
    organize_desc = db.Column(db.String, nullable=False)
    organize_email    