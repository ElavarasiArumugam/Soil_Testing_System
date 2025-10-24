# Soil Testing and Crop Recommendation System

A web application built with Python (Flask) and SQLite that allows farmers, technicians, and admins to manage soil testing and receive crop and fertilizer recommendations.

## Features

* **User Roles:** Separate dashboards and functionalities for Admin, Farmer, and Technician.
* **Soil Sample Management:** Farmers can submit soil samples for testing.
* **Soil Analysis:** Technicians can input soil test results (like pH, N, P, K levels).
* **Recommendation Engine:** Automatically generates crop and fertilizer recommendations based on soil data.
* **Historical Data:** View past soil test results and recommendations.

## Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite (`soil.db`)
* **Frontend:** HTML, CSS, JavaScript

## How to Run This Project

Follow these steps to get a local copy up and running.

### 1. Prerequisites

* [Python 3.10+](https://www.python.org/downloads/)
* Git

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ElavarasiArumugam/Soil_Testing_System.git](https://github.com/ElavarasiArumugam/Soil_Testing_System.git)
    cd Soil_Testing_System/backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install the required packages:**
    *(First, you need to create this file. Run this command in your terminal)*:
    ```bash
    pip freeze > requirements.txt
    ```
    *(Then, add this command to the README for others)*:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    *(I am guessing based on your `db_init.py` file. Change if needed.)*
    ```bash
    python db_init.py
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```
    Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
