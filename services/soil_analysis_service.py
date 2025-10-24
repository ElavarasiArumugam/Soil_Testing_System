# backend/services/soil_analysis_service.py
from app import db
from models.soil_sample import SoilSample

def add_soil_sample(data):
    """
    Adds a new soil sample record to the database.
    """
    new_sample = SoilSample(
        farmer_id=data['farmer_id'],
        nitrogen=data['nitrogen'],
        phosphorus=data['phosphorus'],
        potassium=data['potassium'],
        ph=data['ph'],
        rainfall=data['rainfall']
    )
    db.session.add(new_sample)
    db.session.commit()
    return new_sample

def get_samples_by_farmer(farmer_id):
    """
    Retrieves all soil samples for a specific farmer.
    """
    return SoilSample.query.filter_by(farmer_id=farmer_id).order_by(SoilSample.created_at.desc()).all()