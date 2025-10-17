from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# In-memory storage (replace with DB later)
soil_samples = []
test_results = []

# ------------------- DASHBOARDS -------------------
@app.route('/farmer')
def farmer_dashboard():
    return render_template('farmer_dashboard.html')

@app.route('/technician')
def technician_dashboard():
    return render_template('technician_dashboard.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')


# ------------------- API ENDPOINTS -------------------

# Farmer submits a soil sample
@app.route('/submit_sample', methods=['POST'])
def submit_sample():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    data['id'] = len(soil_samples) + 1
    data['status'] = 'Pending'
    soil_samples.append(data)
    return jsonify({'message': 'Soil sample submitted successfully!', 'data': data}), 201


# Technician submits test results & recommendations
@app.route('/submit_test', methods=['POST'])
def submit_test():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    # Update soil sample by sample_id
    sample_id = int(data.get('sample_id', 0))
    sample = next((s for s in soil_samples if s['id'] == sample_id), None)
    if not sample:
        return jsonify({'error': 'Sample ID not found'}), 404

    sample.update({
        'ph': data.get('ph'),
        'nitrogen': data.get('nitrogen'),
        'phosphorus': data.get('phosphorus'),
        'potassium': data.get('potassium'),
        'moisture': data.get('moisture'),
        'crop_name': data.get('crop_name'),
        'fertilizer_name': data.get('fertilizer_name'),
        'notes': data.get('notes'),
        'status': 'Completed'
    })
    test_results.append(sample)
    return jsonify({'message': 'Test results submitted!', 'data': sample}), 201


# Admin gets crop database
@app.route('/api/admin/crops', methods=['GET'])
def get_crops():
    # Sample seed data (replace with DB query)
    crops = [
        {"crop_name": "Wheat","ideal_pH_min": 6.0,"ideal_pH_max": 7.0,"nitrogen_req":50,"phosphorus_req":30,"potassium_req":20},
        {"crop_name": "Rice","ideal_pH_min": 5.5,"ideal_pH_max": 6.5,"nitrogen_req":60,"phosphorus_req":40,"potassium_req":30},
        {"crop_name": "Maize","ideal_pH_min": 5.5,"ideal_pH_max": 7.0,"nitrogen_req":50,"phosphorus_req":40,"potassium_req":40}
    ]
    return jsonify(crops)


# Technician gets assigned samples
@app.route('/api/technicians/assigned-samples', methods=['GET'])
def get_assigned_samples():
    pending_samples = [s for s in soil_samples if s['status'] == 'Pending']
    return jsonify(pending_samples)


if __name__ == "__main__":
    app.run(debug=True)
