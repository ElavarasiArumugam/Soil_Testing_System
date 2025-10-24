from flask import Blueprint, request, jsonify
from services.recommendation_service import find_matching_crop

recommendation_bp = Blueprint('recommendation_bp', __name__)

@recommendation_bp.route('/', methods=['POST'])
def get_recommendation():
    """
    Endpoint to get a crop recommendation based on soil data.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    required_fields = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'rainfall']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required soil data fields"}), 400

    try:
        ph = float(data['ph'])
        n = float(data['nitrogen'])
        p = float(data['phosphorus'])
        k = float(data['potassium'])
        rainfall = float(data['rainfall'])

        crop_name = find_matching_crop(ph, n, p, k, rainfall)

        return jsonify({"recommended_crop": crop_name})

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data format for soil parameters"}), 400
