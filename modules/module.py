# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(50))
    weight = db.Column(db.Float)
    mileage = db.Column(db.Float)
    specs = db.Column(db.String(255))
    photo = db.Column(db.String(255))
