# Placeholder for authentication routes
# backend/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from models.farmer import Farmer

# Thisa line creates the 'auth_bp' that app.py is looking for
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint for a farmer to log in.
    """
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    # Find the farmer by email in the database
    farmer = Farmer.query.filter_by(email=data['email']).first()

    # Check if the farmer exists and if the password is correct
    if not farmer or not farmer.check_password(data['password']):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # In a real-world application, you would generate and return a JWT token here.
    # For now, we'll return a success message and the farmer's data.
    return jsonify({
        "message": "Login successful", 
        "farmer": farmer.to_dict()
    }), 200
