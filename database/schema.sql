-- Drop tables if they exist to prevent errors on re-run
DROP TABLE IF EXISTS soil_data;
DROP TABLE IF EXISTS crop_recommendations;
DROP TABLE IF EXISTS farmers;
DROP TABLE IF EXISTS technicians;

-- Farmers table
CREATE TABLE IF NOT EXISTS farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    location TEXT,
    password_hash TEXT NOT NULL
);

-- Technicians table
CREATE TABLE IF NOT EXISTS technicians (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Table to store user soil test data
-- This now includes all fields from the farmer and technician forms
CREATE TABLE soil_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER NOT NULL,
    
    -- Fields from Farmer Form
    sample_date TEXT,
    sample_location TEXT,
    remarks TEXT,

    -- Fields from Technician Form (Test Results)
    ph REAL,
    nitrogen REAL,
    phosphorus REAL,
    potassium REAL,
    moisture REAL,

    -- Fields from Technician Form (Recommendation)
    crop_name TEXT,
    fertilizer_name TEXT,
    notes TEXT,

    -- Meta fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Pending', -- To track if results have been added
    FOREIGN KEY (farmer_id) REFERENCES farmers (id)
);

-- Table to store crop recommendation ranges
CREATE TABLE crop_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_name TEXT NOT NULL,
    ph_min REAL,
    ph_max REAL,
    n_min REAL,
    n_max REAL,
    p_min REAL,
    p_max REAL,
    k_min REAL,
    k_max REAL,
    rainfall_min REAL,
    rainfall_max REAL
);

