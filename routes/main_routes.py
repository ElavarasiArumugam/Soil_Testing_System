# routes/main_routes.py (UPDATED)

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from db_init import db
from models.soil_sample import SoilSample

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/submit_sample", methods=["POST"])
@login_required # Protect this route
def submit_sample():
    """
    Handles submission from the farmer_dashboard.html form
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing data"}), 400

        # --- KEY CHANGE ---
        # Get the farmer ID from the logged-in user session
        farmer_id = current_user.id

        sample = SoilSample(
            farmer_id=farmer_id, # Use the ID from the session
            sample_date=data.get('sample_date'),
            sample_location=data.get('sample_location'),
            remarks=data.get('remarks'),
            status='Pending'
        )

        db.session.add(sample)
        db.session.commit()

        return jsonify({"message": "Soil sample submitted successfully!"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500