"""
Database Models for Hospital Management System
Defines all SQLAlchemy ORM models for the application
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Patient(db.Model):
    """Patient model for storing patient information"""
    __tablename__ = 'patients'
    
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert patient object to dictionary"""
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'age': self.age,
            'gender': self.gender,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }



class Doctor(db.Model):
    """Doctor model for storing doctor information and availability"""
    __tablename__ = 'doctors'
    
    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    available_days = db.Column(db.String(50))
    start_time = db.Column(db.TIME)
    end_time = db.Column(db.TIME)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        """Convert doctor object to dictionary"""
        return {
            'doctor_id': self.doctor_id,
            'name': self.name,
            'specialization': self.specialization,
            'email': self.email,
            'phone': self.phone,
            'available_days': self.available_days,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None,
            'is_active': self.is_active
        }



class Appointment(db.Model):
    """Appointment model for storing appointment bookings"""
    __tablename__ = 'appointments'
    
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.TIME, nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    reason = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')
    
    def to_dict(self):
        """Convert appointment object to dictionary"""
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': str(self.appointment_time) if self.appointment_time else None,
            'status': self.status,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'patient': self.patient.to_dict() if self.patient else None,
            'doctor': self.doctor.to_dict() if self.doctor else None
        }



class Resource(db.Model):
    """Resource model for storing hospital resources (beds, equipment, etc.)"""
    __tablename__ = 'resources'
    
    resource_id = db.Column(db.Integer, primary_key=True)
    resource_type = db.Column(db.String(50), nullable=False)
    resource_name = db.Column(db.String(100), nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100))
    
    def to_dict(self):
        """Convert resource object to dictionary"""
        return {
            'resource_id': self.resource_id,
            'resource_type': self.resource_type,
            'resource_name': self.resource_name,
            'total_quantity': self.total_quantity,
            'available_quantity': self.available_quantity,
            'location': self.location
        }



class PatientStatistics(db.Model):
    """PatientStatistics model for storing historical patient data for AI/ML"""
    __tablename__ = 'patient_statistics'
    
    stat_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    patient_count = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        """Convert patient statistics object to dictionary"""
        return {
            'stat_id': self.stat_id,
            'date': self.date.isoformat() if self.date else None,
            'day_of_week': self.day_of_week,
            'patient_count': self.patient_count
        }
