# app.py (COMPLETE AND UPDATED)

import os
from flask import Flask, render_template, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from flask_bcrypt import Bcrypt

from config import Config
from db_init import db

# Import all your models so SQLAlchemy knows about them
from models.crop import CropRecommendation
from models.farmer import Farmer
from models.soil_sample import SoilSample
from models.technician import Technician
from models.admin import Admin

# Import all your blueprints
from routes.admin_routes import admin_bp
from routes.farmer_routes import farmer_bp
from routes.technician_routes import technician_bp
from routes.auth_routes import auth_bp
from routes.recommendation_routes import recommendation_bp
from routes.main_routes import main_bp
from routes.soil_routes import soil_bp

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)
CORS(app)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page" 

# --- UPDATED User Loader (CRITICAL for Flask-Login) ---
# This function tells flask_login how to find a user given their ID
@login_manager.user_loader
def load_user(user_id):
    # Get the user type from the session
    user_type = session.get('user_type')

    if user_type == 'farmer':
        return Farmer.query.get(int(user_id))
    elif user_type == 'technician':
        return Technician.query.get(int(user_id))
    elif user_type == 'admin':
        return Admin.query.get(int(user_id))
    else:
        return None

# Register all your API blueprints
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(farmer_bp, url_prefix='/api/farmer')
app.register_blueprint(technician_bp, url_prefix='/api/technicians')
app.register_blueprint(auth_bp, url_prefix='/api/auth') # Auth routes
app.register_blueprint(recommendation_bp, url_prefix='/api/recommend')
app.register_blueprint(soil_bp, url_prefix='/api/soil')
app.register_blueprint(main_bp) 

# ------------------- HTML ROUTES -------------------

@app.route('/')
def home_page():
    return render_template('index.html')

# --- NEW LOGIN/REGISTER PAGES ---
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

# --- PROTECTED DASHBOARD ROUTES ---
@app.route('/farmer')
@login_required
def farmer_dashboard():
    if not isinstance(current_user, Farmer):
        return redirect(url_for('login_page'))
    return render_template('farmer_dashboard.html')

@app.route('/technician')
@login_required
def technician_dashboard():
    if not isinstance(current_user, Technician):
        return redirect(url_for('login_page'))
    return render_template('technician_dashboard.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        return redirect(url_for('login_page'))
    return render_template('admin_dashboard.html')


# ------------------- DATABASE CREATION & SEEDING -------------------

def create_and_seed_database():
    with app.app_context():
        db.create_all()

        # Seed crops
        if CropRecommendation.query.first() is None:
            print("Seeding crop_recommendations table...")
            seed_crops = [
                ('Rice', 5.0, 6.5, 50, 120, 40, 100, 40, 120, 1000, 3000),
                ('Tea', 4.5, 5.5, 20, 80, 15, 60, 20, 80, 1200, 2500),
                ('Coffee', 5.0, 6.0, 30, 90, 20, 70, 30, 90, 1200, 2000),
                ('Wheat', 6.0, 7.5, 60, 140, 30, 100, 30, 120, 300, 800),
                ('Maize', 5.5, 7.0, 50, 120, 40, 100, 40, 120, 500, 1500),
                ('Groundnut', 5.5, 7.0, 20, 80, 10, 60, 10, 60, 400, 1000),
                ('Soybean', 6.0, 7.5, 40, 120, 20, 80, 20, 80, 400, 1200),
                ('Barley', 7.0, 8.0, 40, 100, 20, 80, 20, 80, 300, 700),
                ('Mustard', 7.0, 8.5, 30, 80, 20, 60, 20, 60, 300, 700),
                ('Cotton', 7.0, 8.0, 40, 120, 30, 80, 30, 100, 500, 1200),
                ('Millet', 5.5, 7.5, 10, 50, 5, 30, 10, 50, 200, 600),
                ('Sorghum', 5.5, 7.5, 10, 60, 5, 35, 10, 60, 200, 700),
                ('Cassava', 5.0, 7.0, 10, 50, 5, 30, 10, 50, 500, 1500),
                ('Sweet Potato', 5.5, 7.5, 15, 60, 5, 40, 10, 60, 400, 1000),
                ('Tomato', 6.0, 7.0, 30, 90, 20, 60, 20, 60, 400, 1200),
                ('Potato', 5.5, 6.5, 40, 100, 30, 80, 20, 80, 500, 1200),
                ('Carrot', 6.0, 7.5, 20, 70, 20, 50, 20, 50, 400, 1000)
            ]
            
            for crop_data in seed_crops:
                crop = CropRecommendation(
                    crop_name=crop_data[0],
                    ph_min=crop_data[1], ph_max=crop_data[2],
                    n_min=crop_data[3], n_max=crop_data[4],
                    p_min=crop_data[5], p_max=crop_data[6],
                    k_min=crop_data[7], k_max=crop_data[8],
                    rainfall_min=crop_data[9], rainfall_max=crop_data[10]
                )
                db.session.add(crop)
            db.session.commit()
            print("Crops seeded.")

        # Seed a default Admin and Technician user for testing
        if Admin.query.first() is None:
            print("Seeding default Admin user...")
            admin_user = Admin(email='admin@app.com')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created: admin@app.com, Pass: admin123")
        else:
            print("Admin user already exists.")

        if Technician.query.first() is None:
            print("Seeding default Technician user...")
            tech_user = Technician(name='Test Tech', email='tech@app.com')
            tech_user.set_password('tech123')
            db.session.add(tech_user)
            db.session.commit()
            print("Technician user created: tech@app.com, Pass: tech123")
        else:
            print("Technician user already exists.")
        
        print("Database seeding check complete.")


if __name__ == "__main__":
    # The database is created, no need to delete it every time
    # if os.path.exists(os.path.join(Config.BASE_DIR, 'soil.db')):
    #     print("Deleting old database to apply new schema...")
    #     os.remove(os.path.join(Config.BASE_DIR, 'soil.db'))
        
    create_and_seed_database() # This will just create if not exists
    app.run(debug=True)