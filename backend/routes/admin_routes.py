from flask import Blueprint, jsonify
from models.crop import CropRecommendation

admin_bp = Blueprint('admin_bp', __name__)

# NEW ENDPOINT FOR: GET /api/crops
@admin_bp.route('/crops', methods=['GET'])
def get_all_crops():
    """Endpoint for an admin to get a list of all crop recommendations."""
    try:
        crops = CropRecommendation.query.all()
        return jsonify([crop.to_dict() for crop in crops]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
