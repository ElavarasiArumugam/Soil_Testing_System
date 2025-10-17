from flask import Blueprint, request, jsonify
from app import db
from models.farmer import Farmer

farmer_bp = Blueprint('farmer_bp', __name__)

@farmer_bp.route('/register', methods=['POST'])
def register_farmer():
    """Endpoint to register a new farmer."""
    data = request.get_json()
    if not data or not all(k in data for k in ['name', 'email', 'password']):
        return jsonify({"error": "Missing data"}), 400
    
    if Farmer.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email address already in use"}), 409

    new_farmer = Farmer(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        location=data.get('location')
    )
    new_farmer.set_password(data['password'])
    
    db.session.add(new_farmer)
    db.session.commit()
    
    return jsonify(new_farmer.to_dict()), 201
