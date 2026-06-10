Soil Testing and Crop Recommendation System

A web application built using Python (Flask) and SQLite that helps farmers, technicians, and admins manage soil testing data and get crop and fertilizer recommendations based on soil parameters.

Live Demo

https://soil-testing-system.onrender.com

Features
Multi-Role System
Separate dashboards for Admin, Farmer, and Technician
Role-based access control
Soil Sample Management
Farmers can submit soil samples for testing
Track soil test history and status
Soil Analysis Module
Technicians input soil parameters:
pH level
Nitrogen (N)
Phosphorus (P)
Potassium (K)
Recommendation Engine
Suggests suitable crops
Suggests fertilizers
Based on soil nutrient analysis
Historical Data Tracking
View previous soil test results
Track recommendation history
Tech Stack

Backend: Python, Flask
Database: SQLite (soil.db)
Frontend: HTML, CSS, JavaScript

How It Works
Farmer submits soil details
Technician enters lab test values (N, P, K, pH)
System processes data
Recommendations are generated
Results are stored and displayed
Run Locally
1. Clone the repository

git clone https://github.com/ElavarasiArumugam/Soil_Testing_System.git
cd Soil_Testing_System/backend

2. Create virtual environment

python -m venv .venv
.venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Initialize database

python db_init.py

5. Run application

python app.py

6. Open in browser

http://127.0.0.1:5000

Demo Credentials

Admin
Email: admin@example.com
Password: admin123

Farmer
Email: farmer@example.com
Password: farmer123

Technician
Email: tech@example.com
Password: tech123

Deployment

https://soil-testing-system.onrender.com

Future Improvements
Machine learning-based crop prediction
Weather-based recommendations
REST API support
Improved UI and dashboards
About

A web application built using Flask and SQLite that connects farmers, technicians, and admins. It manages soil testing and generates automated crop and fertilizer recommendations.
