from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
import datetime
import random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    media = db.relationship('Media', backref='owner', lazy=True)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    media_type = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    director = db.Column(db.String(100))
    # Additional fields
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Authentication decorator using JWT
def token_required(f):
    @wraps(f)
    