# backend/app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import Config

# Initialize extensions
db = SQLAlchemy()

def create_app(config_class=Config):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS to allow frontend to connect
    CORS(app)

    # Initialize extensions with app
    db.init_app(app)

    # --- Import and register all blueprints ---
    from routes.recommendation_routes import recommendation_bp
    from routes.soil_routes import soil_bp
    from routes.farmer_routes import farmer_bp
    from routes.auth_routes import auth_bp
    from routes.admin_routes import admin_bp
    from routes.technician_routes import technician_bp

    # Register blueprints with their URL prefixes
    app.register_blueprint(recommendation_bp, url_prefix='/api/recommendations')
    app.register_blueprint(soil_bp, url_prefix='/api/soil')
    app.register_blueprint(farmer_bp, url_prefix='/api/farmers')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(technician_bp, url_prefix='/api/technicians')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
