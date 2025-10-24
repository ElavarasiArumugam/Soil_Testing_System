# routes/farmer_routes.py (CORRECTED AND FINAL)

from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models.soil_sample import SoilSample

farmer_bp = Blueprint('farmer_bp', __name__)

@farmer_bp.route('/my_samples', methods=['GET'])
@login_required
def get_my_samples():
    """
    Returns a list of all soil samples submitted by the
    currently logged-in farmer, ordered by most recent.
    """
    try:
        # We filter by the logged-in user's ID and order by ID descending
        samples = SoilSample.query.filter_by(farmer_id=current_user.id).order_by(SoilSample.id.desc()).all()
        
        # Return the list of samples as JSON
        return jsonify([sample.to_dict() for sample in samples]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500