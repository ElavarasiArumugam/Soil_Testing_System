# models/soil_sample.py (UPDATED)

from db_init import db

class SoilSample(db.Model):
    __tablename__ = 'soil_samples'

    id = db.Column(db.Integer, primary_key=True)
    
    # --- Link to Farmer ---
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)

    # --- Sample Info (from Farmer) ---
    sample_date = db.Column(db.String(50))
    sample_location = db.Column(db.String(200))
    remarks = db.Column(db.Text)

    # --- Test Results (from Technician) ---
    ph = db.Column(db.Float)
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    moisture = db.Column(db.Float)

    # --- Recommendation (from Technician) ---
    recommended_crop = db.Column(db.String(100))
    recommended_fertilizer = db.Column(db.String(100))
    recommendation_notes = db.Column(db.Text)

    # --- Meta Fields ---
    status = db.Column(db.String(50), default='Pending')


    def to_dict(self):
        # We can get farmer info from the 'backref'
        farmer_name = self.farmer.name if self.farmer else 'N/A'
        
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "farmer_name": farmer_name, # Added this field
            "sample_date": self.sample_date,
            "sample_location": self.sample_location,
            "remarks": self.remarks,
            "ph": self.ph,
            "nitrogen": self.nitrogen,
            "phosphorus": self.phosphorus,
            "potassium": self.potassium,
            "moisture": self.moisture,
            "recommended_crop": self.recommended_crop,
            "recommended_fertilizer": self.recommended_fertilizer,
            "recommendation_notes": self.recommendation_notes,
            "status": self.status
        }