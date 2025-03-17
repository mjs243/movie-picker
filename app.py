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
    def decorated(*args, **kwargs):
        token = None
        # Extract token from Auth header
        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            parts = bearer.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                raise Exception('User not found!')
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Routes for User Registration and Login
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required!'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists!'}), 400
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required!'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials!'}), 401
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200

# CRUD Endpoints for Media
@app.route('/media', methods=['POST'])
@token_required





@app.route('/media', methods=['GET'])
@token_required




@app.route('/media/<int:media_id>', methods=['PUT'])
@token_required



@app.route('/media/<int:media_id>', methods=['DELETE'])
@token_required




@app.route('/random', methods=['GET'])
@token_required




# Endpoint to Import Media via JSON Array
@app.route('/import', methods=['POST'])
@token_required





# Global Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found!'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'An internal error occurred!'}), 500

if __name__ == '__main__':
    with app.app_content():
        db.create_all()
    app.run(debug=True)