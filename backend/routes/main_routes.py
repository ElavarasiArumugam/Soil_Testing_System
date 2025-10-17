from flask import Blueprint, request, jsonify
from app import db
from models.soil_sample import SoilSample

# This blueprint is now designed to work perfectly with the modern JavaScript Fetch API.
main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/submit_sample', methods=['POST'])
def submit_sample():
    """
    Handles the modern fetch() submission from the farmer_dashboard.html.
    It receives form data and returns a clean JSON response.
    """
    try:
        # Create a new SoilSample object using the data from the form.
        # request.form.get() correctly reads the FormData sent by the fetch command.
        new_sample = SoilSample(
            farmer_name=request.form.get('name'),
            farmer_location=request.form.get('location'),
            contact_type=request.form.get('contact_type'),
            contact_value=request.form.get('contact_value'),
            sample_date=request.form.get('sample_date'),
            sample_location=request.form.get('sample_location'),
            remarks=request.form.get('remarks'),
            status='Pending'  # Set the initial status for the technician.
        )
        
        db.session.add(new_sample)
        db.session.commit()

        # **THIS IS THE CRITICAL FIX:**
        # We return a JSON success message with a 200 OK status.
        # This is exactly what the main.js file's fetch().then(...) logic is expecting.
        return jsonify({"message": "Sample submitted successfully"}), 200

    except Exception as e:
        # If any error occurs, print it to the terminal for debugging.
        print(f"DATABASE ERROR in /submit_sample: {e}")
        # Return a JSON error message with a 500 status code.
        return jsonify({"error": "An internal server error occurred"}), 500

@main_bp.route('/submit_test', methods=['POST'])
def submit_test():
    """
    Handles the modern fetch() submission from the technician_dashboard.html.
    It finds an existing sample, updates it, and returns a JSON response.
    """
    try:
        sample_id = request.form.get('sample_id')
        if not sample_id:
            return jsonify({"error": "Sample ID is required"}), 400

        # Find the existing sample in the database by its ID.
        sample = SoilSample.query.get(sample_id)
        if not sample:
            return jsonify({"error": f"Sample with ID {sample_id} not found"}), 404

        # Update the sample's attributes with the new data from the form.
        sample.ph = request.form.get('ph')
        sample.nitrogen = request.form.get('nitrogen')
        sample.phosphorus = request.form.get('phosphorus')
        sample.potassium = request.form.get('potassium')
        sample.moisture = request.form.get('moisture')
        sample.crop_name = request.form.get('crop_name')
        sample.fertilizer_name = request.form.get('fertilizer_name')
        sample.notes = request.form.get('notes')
        sample.status = 'Completed'

        db.session.commit()
        
        # **THIS IS THE CRITICAL FIX:**
        # Return a JSON success message instead of a redirect.
        return jsonify({"message": "Test results submitted successfully"}), 200
        
    except Exception as e:
        print(f"DATABASE ERROR in /submit_test: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

