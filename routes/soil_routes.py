from flask import Blueprint, request, jsonify
from db_init import db
from models.soil_sample import SoilSample

soil_bp = Blueprint('soil_bp', __name__)

@soil_bp.route("/samples", methods=["GET"])
def get_samples():
    samples = SoilSample.query.all()
    return jsonify([s.to_dict() for s in samples]), 200

@soil_bp.route("/samples", methods=["POST"])
def create_sample():
    data = request.get_json()
    sample = SoilSample(**data)
    db.session.add(sample)
    db.session.commit()
    return jsonify(sample.to_dict()), 201
