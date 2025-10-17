from flask import Blueprint, request, jsonify
from app import db
from models.soil_sample import SoilSample
# ... (other imports)

technician_bp = Blueprint('technician_bp', __name__)

# ... (login/register routes)

# NEW ENDPOINT FOR: GET /api/assigned_samples
@technician_bp.route('/assigned_samples', methods=['GET'])
def get_assigned_samples():
    """
    Returns a list of all soil samples that have not yet been analyzed.
    (i.e., nitrogen, ph, etc. are NULL)
    """
    try:
        # A sample is "assigned" if it has no test results yet
        samples = SoilSample.query.filter(SoilSample.ph == None).all()
        return jsonify([sample.to_dict() for sample in samples]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATED ENDPOINT FOR: POST /api/submit_test
@technician_bp.route('/submit-test/<int:sample_id>', methods=['POST'])
def submit_test(sample_id):
    """
    Endpoint for a technician to submit test results and recommendations
    for a specific sample.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    sample = SoilSample.query.get(sample_id)
    if not sample:
        return jsonify({"error": "Sample not found"}), 404

    # Update sample with test results from the form
    sample.ph = data.get('ph')
    sample.nitrogen = data.get('nitrogen')
    sample.phosphorus = data.get('phosphorus')
    sample.potassium = data.get('potassium')
    sample.moisture = data.get('moisture')
    
    # Update with recommendations
    sample.recommended_crop = data.get('crop_name')
    sample.recommended_fertilizer = data.get('fertilizer_name')
    sample.recommendation_notes = data.get('notes')

    db.session.commit()
    return jsonify(sample.to_dict()), 200
