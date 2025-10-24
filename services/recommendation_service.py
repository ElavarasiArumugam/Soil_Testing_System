# backend/services/recommendation_service.py
from models.crop import CropRecommendation

def find_matching_crop(ph, n, p, k, rainfall):
    """
    Finds a suitable crop based on soil and weather conditions.
    """
    crop = CropRecommendation.query.filter(
        CropRecommendation.ph_min <= ph, CropRecommendation.ph_max >= ph,
        CropRecommendation.n_min <= n, CropRecommendation.n_max >= n,
        CropRecommendation.p_min <= p, CropRecommendation.p_max >= p,
        CropRecommendation.k_min <= k, CropRecommendation.k_max >= k,
        CropRecommendation.rainfall_min <= rainfall, CropRecommendation.rainfall_max >= rainfall
    ).first()

    return crop.crop_name if crop else "No suitable crop found"