# routes/admin_routes.py

from flask import Blueprint, jsonify
from models.crop import CropRecommendation
from models.soil_sample import SoilSample  # <--- IMPORT THIS

admin_bp = Blueprint('admin_bp', __name__)

# This is your existing endpoint
@admin_bp.route('/crops', methods=['GET'])
def get_all_crops():
    """Endpoint for an admin to get a list of all crop recommendations."""
    try:
        crops = CropRecommendation.query.all()
        return jsonify([crop.to_dict() for crop in crops]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- ADD THIS NEW ENDPOINT ---
@admin_bp.route('/all_samples', methods=['GET'])
def get_all_samples():
    """Endpoint for an admin to get a list of all soil samples."""
    try:
        # Query all samples from the SoilSample table
        samples = SoilSample.query.all()
        # Return them as a list of dictionaries
        return jsonify([sample.to_dict() for sample in samples]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500