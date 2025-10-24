from db_init import db

class CropRecommendation(db.Model):
    __tablename__ = 'crop_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    ph_min = db.Column(db.Float)
    ph_max = db.Column(db.Float)
    n_min = db.Column(db.Float)
    n_max = db.Column(db.Float)
    p_min = db.Column(db.Float)
    p_max = db.Column(db.Float)
    k_min = db.Column(db.Float)
    k_max = db.Column(db.Float)
    rainfall_min = db.Column(db.Float)
    rainfall_max = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'ph_range': (self.ph_min, self.ph_max),
            'nitrogen_range': (self.n_min, self.n_max),
            'phosphorus_range': (self.p_min, self.p_max),
            'potassium_range': (self.k_min, self.k_max),
            'rainfall_range': (self.rainfall_min, self.rainfall_max)
        }
