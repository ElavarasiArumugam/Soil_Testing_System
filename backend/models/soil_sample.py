# backend/models/soil_sample.py
from app import db
from datetime import datetime

class SoilSample(db.Model):
    __tablename__ = 'soil_data'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    
    # Existing fields
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    ph = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    
    # New fields to match the schema
    moisture = db.Column(db.Float)
    sample_date = db.Column(db.String)
    sample_location = db.Column(db.String)
    remarks = db.Column(db.String)
    
    # Recommendation fields
    recommended_crop = db.Column(db.String)
    recommended_fertilizer = db.Column(db.String)
    recommendation_notes = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'ph': self.ph,
            'rainfall': self.rainfall,
            'moisture': self.moisture,
            'sample_date': self.sample_date,
            'sample_location': self.sample_location,
            'remarks': self.remarks,
            'recommended_crop': self.recommended_crop,
            'recommended_fertilizer': self.recommended_fertilizer,
            'recommendation_notes': self.recommendation_notes,
            'created_at': self.created_at.isoformat()
        }
