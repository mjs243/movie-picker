from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
import datetime
import random
from werkzeug.security import generate_password_hash, check_password_hash

