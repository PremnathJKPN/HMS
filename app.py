"""
Hospital Appointment and Resource Optimization Intelligence System
Main Flask Application
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime, time, date, timedelta
import os
from dotenv import load_dotenv
from models import db, Doctor, Resource, PatientStatistics

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Database Configuration - Using SQLite for easy setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Import routes
from routes import (
    patient_bp,
    doctor_bp,
    appointment_bp,
    resource_bp,
    ai_bp,
    admin_bp
)

def init_db():
    """
    Initialize database with sample data
    Creates tables and populates them with initial data if empty
    """
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if Doctor.query.count() > 0:
            print("Database already initialized.")
            return
        
        # Add sample doctors
        doctors = [
            Doctor(
                name='Dr. Smith',
                specialization='Cardiology',
                email='smith@hospital.com',
                phone='1234567890',
                available_days='Monday,Wednesday,Friday',
                start_time=time(9, 0),
                end_time=time(17, 0)
            ),
            Doctor(
                name='Dr. Johnson',
                specialization='Neurology',
                email='johnson@hospital.com',
                phone='0987654321',
                available_days='Tuesday,Thursday',
                start_time=time(10, 0),
                end_time=time(18, 0)
            ),
            Doctor(
                name='Dr. Williams',
                specialization='Orthopedics',
                email='williams@hospital.com',
                phone='1122334455',
                available_days='Monday,Tuesday,Wednesday,Thursday,Friday',
                start_time=time(8, 0),
                end_time=time(16, 0)
            )
        ]
        
        # Add sample resources
        resources = [
            Resource(
                resource_type='Bed',
                resource_name='General Ward Bed',
                total_quantity=50,
                available_quantity=45,
                location='Ground Floor'
            ),
            Resource(
                resource_type='Bed',
                resource_name='ICU Bed',
                total_quantity=10,
                available_quantity=8,
                location='First Floor'
            ),
            Resource(
                resource_type='Equipment',
                resource_name='X-Ray Machine',
                total_quantity=2,
                available_quantity=2,
                location='Basement'
            ),
            Resource(
                resource_type='Equipment',
                resource_name='MRI Machine',
                total_quantity=1,
                available_quantity=1,
                location='First Floor'
            ),
            Resource(
                resource_type='Room',
                resource_name='Operation Theater',
                total_quantity=3,
                available_quantity=3,
                location='Second Floor'
            )
        ]
        
        # Add sample patient statistics for AI/ML
        stats = []
        base_date = date(2024, 1, 1)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        counts = [100, 60, 80, 70, 90, 40, 30]
        
        for i in range(14):
            stat_date = base_date + timedelta(days=i)
            stats.append(PatientStatistics(
                date=stat_date,
                day_of_week=days[stat_date.weekday()],
                patient_count=counts[stat_date.weekday()]
            ))
        
        # Commit all data
        db.session.add_all(doctors)
        db.session.add_all(resources)
        db.session.add_all(stats)
        db.session.commit()
        print("Database initialized with sample data!")

# Register blueprints
app.register_blueprint(patient_bp, url_prefix='/api/patients')
app.register_blueprint(doctor_bp, url_prefix='/api/doctors')
app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
app.register_blueprint(resource_bp, url_prefix='/api/resources')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(admin_bp, url_prefix='/api/admin')


@app.route('/')
def home():
    """Render the main dashboard page"""
    return render_template('index.html')


@app.route('/api')
def api_info():
    """Return API information and available endpoints"""
    return jsonify({
        'message': 'Hospital Appointment and Resource Optimization Intelligence System',
        'version': '1.0',
        'endpoints': {
            'patients': '/api/patients',
            'doctors': '/api/doctors',
            'appointments': '/api/appointments',
            'resources': '/api/resources',
            'ai': '/api/ai',
            'admin': '/api/admin'
        }
    })


if __name__ == '__main__':
    # Initialize database and run the application
    init_db()
    app.run(debug=True, port=5000)
