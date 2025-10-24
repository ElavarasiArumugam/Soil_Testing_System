# routes/auth_routes.py (UPDATED)

from flask import Blueprint, request, jsonify, session # <-- Import session
from flask_login import login_user, logout_user, login_required
from db_init import db
from models.farmer import Farmer
from models.technician import Technician
from models.admin import Admin

auth_bp = Blueprint('auth_bp', __name__)

# ... (Your register_farmer function is unchanged) ...
@auth_bp.route('/register', methods=['POST'])
def register_farmer():
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


@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint for any user (Farmer, Tech, Admin) to log in."""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    email = data['email']
    password = data['password']
    
    # 1. Try to find a Farmer
    user = Farmer.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        session['user_type'] = 'farmer' # <-- ADD THIS LINE
        return jsonify({
            "message": "Farmer login successful", 
            "dashboard_url": "/farmer"
        }), 200

    # 2. Try to find a Technician
    user = Technician.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        session['user_type'] = 'technician' # <-- ADD THIS LINE
        return jsonify({
            "message": "Technician login successful", 
            "dashboard_url": "/technician"
        }), 200

    # 3. Try to find an Admin
    user = Admin.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        session['user_type'] = 'admin' # <-- ADD THIS LINE
        return jsonify({
            "message": "Admin login successful", 
            "dashboard_url": "/admin"
        }), 200

    # If no user is found
    return jsonify({"error": "Invalid email or password"}), 401


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logs out the current user."""
    session.pop('user_type', None) # <-- ADD THIS LINE to clear the session
    logout_user()
    return jsonify({"message": "Logout successful"}), 200