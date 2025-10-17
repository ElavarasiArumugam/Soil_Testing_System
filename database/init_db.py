import sqlite3
import os

# Path for the database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'soil_testing.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Execute schema.sql
    schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_file, 'r') as f:
        cursor.executescript(f.read())

    # Execute seed_data.sql
    seed_file = os.path.join(os.path.dirname(__file__), 'seed_data.sql')
    with open(seed_file, 'r') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at {DB_PATH}")

if __name__ == "__main__":
    init_db()
