from flask import Blueprint, request, jsonify
from utils.db_init import db
from models.soil_sample import SoilSample

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/submit_sample", methods=["POST"])
def submit_sample():
    try:
        farmer_name = request.form.get("farmer_name")
        nitrogen = float(request.form.get("nitrogen", 0))
        phosphorus = float(request.form.get("phosphorus", 0))
        potassium = float(request.form.get("potassium", 0))
        ph = float(request.form.get("ph", 0))
        rainfall = float(request.form.get("rainfall", 0))

        sample = SoilSample(
            farmer_name=farmer_name,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            ph=ph,
            rainfall=rainfall
        )

        db.session.add(sample)
        db.session.commit()

        return jsonify({"message": "Soil sample submitted successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
