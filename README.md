Expense Tracker Web Application (Flask)

A secure, full-stack Expense Tracker Web Application built using Flask, enabling users to register, log in, and manage personal income and expenses with category-wise tracking.

The application implements user authentication, database persistence, and deployment-ready configuration.

Features:
User Registration & Login (Flask-Login),
Secure password hashing (Werkzeug),
Add income and expense transactions,
Category-wise expense tracking,
User-specific data isolation,
SQLite database integration,
Production-ready deployment using Gunicorn,
Clean UI with HTML, CSS, and JavaScript

Tech Stack:

Layer Technology
Backend Flask (Python)
Authentication Flask-Login
Database SQLite
Frontend HTML, CSS, JavaScript
Server Gunicorn
Deployment Render

Project Structure:

expense-tracker/
│
├── app.py
├── database.db
├── requirements.txt
├── render.yaml
│
├── templates/
│ ├── login.html
│ ├── register.html
│ └── dashboard.html
│
├── static/
│ ├── style.css
│ └── main.js
│
└── README.md

Installation & Setup (Local):

1. Clone Repository
   git clone https://github.com/shruti07-byte/expense-tracker-flask.git
   cd expense-tracker-flask

2. Create Virtual Environment
   python -m venv venv
   venv\Scripts\activate

3. Install Dependencies
   pip install -r requirements.txt

4. Run Application
   python app.py

Deployment:

The application is deployed on Render using Gunicorn as the production server.
