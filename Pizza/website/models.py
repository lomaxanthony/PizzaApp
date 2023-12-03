from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_size = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='orders')
    pizza_price = db.Column(db.String(50), nullable=False)
    toppings = db.Column(db.PickleType)
