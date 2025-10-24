# routes/technician_routes.py (UPDATED)

from flask import Blueprint, request, jsonify
from db_init import db
from models.soil_sample import SoilSample
from models.crop import CropRecommendation  # <--- IMPORT CROP MODEL

technician_bp = Blueprint('technician_bp', __name__)

# ... (your get_assigned_samples route is here) ...
@technician_bp.route('/assigned_samples', methods=['GET'])
def get_assigned_samples():
    """
    Returns a list of all soil samples that have not yet been analyzed.
    (i.e., status is 'Pending')
    """
    try:
        samples = SoilSample.query.filter_by(status='Pending').all()
        return jsonify([sample.to_dict() for sample in samples]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@technician_bp.route('/submit_test', methods=['POST'])
def submit_test():
    """
    Endpoint for a technician to submit test results.
    The crop recommendation is now calculated automatically.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    sample_id = data.get('sample_id')
    if not sample_id:
        return jsonify({"error": "Missing sample_id"}), 400

    try:
        sample = SoilSample.query.get(int(sample_id))
        if not sample:
            return jsonify({"error": "Sample not found"}), 404

        # Update sample with test results from the form
        sample.ph = data.get('ph')
        sample.nitrogen = data.get('nitrogen')
        sample.phosphorus = data.get('phosphorus')
        sample.potassium = data.get('potassium')
        sample.moisture = data.get('moisture')
        
        # --- NEW: Automatic Recommendation Logic ---
        try:
            ph = float(sample.ph)
            n = float(sample.nitrogen)
            p = float(sample.phosphorus)
            k = float(sample.potassium)

            # Find a matching crop from the database
            matching_crop = CropRecommendation.query.filter(
                CropRecommendation.ph_min <= ph,
                CropRecommendation.ph_max >= ph,
                CropRecommendation.n_min <= n,
                CropRecommendation.n_max >= n,
                CropRecommendation.p_min <= p,
                CropRecommendation.p_max >= p,
                CropRecommendation.k_min <= k,
                CropRecommendation.k_max >= k
            ).first()

            if matching_crop:
                sample.recommended_crop = matching_crop.crop_name
            else:
                sample.recommended_crop = "No suitable crop found"
                
        except (ValueError, TypeError):
            sample.recommended_crop = "Invalid test data"
        # --- END of new logic ---
        
        # Update with recommendations (fertilizer is still manual)
        sample.recommended_fertilizer = data.get('fertilizer_name')
        sample.recommendation_notes = data.get('notes')
        sample.status = 'Completed'

        db.session.commit()
        return jsonify({"message": "Test results submitted!"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500