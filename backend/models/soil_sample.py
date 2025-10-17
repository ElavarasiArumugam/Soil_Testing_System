from utils.db_init import db

class SoilSample(db.Model):
    __tablename__ = 'soil_samples'

    id = db.Column(db.Integer, primary_key=True)
    farmer_name = db.Column(db.String(100))
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    ph = db.Column(db.Float)
    rainfall = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "farmer_name": self.farmer_name,
            "nitrogen": self.nitrogen,
            "phosphorus": self.phosphorus,
            "potassium": self.potassium,
            "ph": self.ph,
            "rainfall": self.rainfall
        }
