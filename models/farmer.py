# models/farmer.py (UPDATED)

from db_init import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Farmer(db.Model, UserMixin):
    __tablename__ = 'farmers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(200))
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship to soil samples (This will work now)
    soil_samples = db.relationship('SoilSample', backref='farmer', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location
        }