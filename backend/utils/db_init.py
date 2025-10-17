import sqlite3
import os

# Get the absolute path of the directory where this script is located (i.e., .../backend/utils)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Go up TWO levels to get the main project directory (from 'utils' to 'backend' to the root)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

# Now, build the correct path to the 'database' directory from the project root
DB_DIR = os.path.join(project_root, 'database')
DB_PATH = os.path.join(DB_DIR, 'app.db')
SCHEMA_PATH = os.path.join(DB_DIR, 'schema.sql')
SEED_PATH = os.path.join(DB_DIR, 'seed_data.sql')

def initialize_database():
    """Creates and seeds the database using the correct paths."""
    # Ensure the database directory exists
    os.makedirs(DB_DIR, exist_ok=True)
    
    # Remove old database file if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read and execute the schema SQL file
    print("Creating tables...")
    with open(SCHEMA_PATH, 'r') as f:
        cursor.executescript(f.read())
    print("Tables created successfully.")

    # Read and execute the seed data SQL file
    print("Seeding data...")
    with open(SEED_PATH, 'r') as f:
        cursor.executescript(f.read())
    print("Data seeded successfully.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database initialized at '{DB_PATH}'")

if __name__ == '__main__':
    initialize_database()