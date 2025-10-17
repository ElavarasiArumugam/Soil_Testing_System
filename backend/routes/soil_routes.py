# backend/routes/soil_routes.py
from flask import Blueprint, request, jsonify
from services.soil_analysis_service import add_soil_sample, get_samples_by_farmer

soil_bp = Blueprint('soil_bp', __name__)

@soil_bp.route('/samples', methods=['POST'])
def create_soil_sample():
    """
    Endpoint to create a new soil sample.
    """
    data = request.get_json()
    if not data or not all(k in data for k in ['farmer_id', 'nitrogen', 'phosphorus', 'potassium', 'ph', 'rainfall']):
        return jsonify({"error": "Missing data"}), 400

    try:
        sample = add_soil_sample(data)
        return jsonify(sample.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@soil_bp.route('/samples/farmer/<int:farmer_id>', methods=['GET'])
def get_farmer_samples(farmer_id):
    """
    Endpoint to get all soil samples for a given farmer.
    """
    try:
        samples = get_samples_by_farmer(farmer_id)
        return jsonify([sample.to_dict() for sample in samples]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500