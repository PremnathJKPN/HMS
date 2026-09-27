"""
API Routes for Hospital Management System
Defines all Flask blueprints and route handlers
"""

from flask import Blueprint, jsonify, request
from models import db, Patient, Doctor, Appointment, Resource, PatientStatistics
from datetime import datetime, time

# ============================================================================
# Patient Routes
# ============================================================================
patient_bp = Blueprint('patients', __name__)


@patient_bp.route('/', methods=['GET'])
def get_patients():
    """Get all patients"""
    patients = Patient.query.all()
    return jsonify([p.to_dict() for p in patients])


@patient_bp.route('/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get a specific patient by ID"""
    patient = Patient.query.get_or_404(patient_id)
    return jsonify(patient.to_dict())


@patient_bp.route('/', methods=['POST'])
def create_patient():
    """Create a new patient"""
    data = request.json
    patient = Patient(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        age=data.get('age'),
        gender=data.get('gender'),
        address=data.get('address')
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201


@patient_bp.route('/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update an existing patient"""
    patient = Patient.query.get_or_404(patient_id)
    data = request.json
    patient.name = data.get('name', patient.name)
    patient.email = data.get('email', patient.email)
    patient.phone = data.get('phone', patient.phone)
    patient.age = data.get('age', patient.age)
    patient.gender = data.get('gender', patient.gender)
    patient.address = data.get('address', patient.address)
    db.session.commit()
    return jsonify(patient.to_dict())


@patient_bp.route('/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a patient"""
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient deleted successfully'})



# ============================================================================
# Doctor Routes
# ============================================================================
doctor_bp = Blueprint('doctors', __name__)


@doctor_bp.route('/', methods=['GET'])
def get_doctors():
    """Get all active doctors"""
    doctors = Doctor.query.filter_by(is_active=True).all()
    return jsonify([d.to_dict() for d in doctors])


@doctor_bp.route('/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    """Get a specific doctor by ID"""
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify(doctor.to_dict())


@doctor_bp.route('/', methods=['POST'])
def create_doctor():
    """Create a new doctor"""
    data = request.json
    start_time = None
    end_time = None
    if data.get('start_time'):
        hour, minute = map(int, data['start_time'].split(':'))
        start_time = time(hour, minute)
    if data.get('end_time'):
        hour, minute = map(int, data['end_time'].split(':'))
        end_time = time(hour, minute)
    
    doctor = Doctor(
        name=data['name'],
        specialization=data['specialization'],
        email=data['email'],
        phone=data['phone'],
        available_days=data.get('available_days'),
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(doctor)
    db.session.commit()
    return jsonify(doctor.to_dict()), 201


@doctor_bp.route('/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    """Update an existing doctor"""
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.json
    doctor.name = data.get('name', doctor.name)
    doctor.specialization = data.get('specialization', doctor.specialization)
    doctor.email = data.get('email', doctor.email)
    doctor.phone = data.get('phone', doctor.phone)
    doctor.available_days = data.get('available_days', doctor.available_days)
    if data.get('start_time'):
        hour, minute = map(int, data['start_time'].split(':'))
        doctor.start_time = time(hour, minute)
    if data.get('end_time'):
        hour, minute = map(int, data['end_time'].split(':'))
        doctor.end_time = time(hour, minute)
    doctor.is_active = data.get('is_active', doctor.is_active)
    db.session.commit()
    return jsonify(doctor.to_dict())


@doctor_bp.route('/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    """Deactivate a doctor (soft delete)"""
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_active = False
    db.session.commit()
    return jsonify({'message': 'Doctor deactivated successfully'})



# ============================================================================
# Appointment Routes
# ============================================================================
appointment_bp = Blueprint('appointments', __name__)


@appointment_bp.route('/', methods=['GET'])
def get_appointments():
    """Get all appointments"""
    appointments = Appointment.query.all()
    return jsonify([a.to_dict() for a in appointments])


@appointment_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Get a specific appointment by ID"""
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify(appointment.to_dict())


@appointment_bp.route('/', methods=['POST'])
def create_appointment():
    """Book a new appointment"""
    data = request.json
    hour, minute = map(int, data['appointment_time'].split(':'))
    appointment = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        appointment_date=datetime.strptime(data['appointment_date'], '%Y-%m-%d').date(),
        appointment_time=time(hour, minute),
        reason=data.get('reason')
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify(appointment.to_dict()), 201


@appointment_bp.route('/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """Update an existing appointment"""
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.json
    if 'status' in data:
        appointment.status = data['status']
    if 'appointment_date' in data:
        appointment.appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
    if 'appointment_time' in data:
        hour, minute = map(int, data['appointment_time'].split(':'))
        appointment.appointment_time = time(hour, minute)
    if 'reason' in data:
        appointment.reason = data['reason']
    db.session.commit()
    return jsonify(appointment.to_dict())


@appointment_bp.route('/<int:appointment_id>', methods=['DELETE'])
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'cancelled'
    db.session.commit()
    return jsonify({'message': 'Appointment cancelled successfully'})


@appointment_bp.route('/patient/<int:patient_id>', methods=['GET'])
def get_patient_appointments(patient_id):
    """Get all appointments for a specific patient"""
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    return jsonify([a.to_dict() for a in appointments])


@appointment_bp.route('/doctor/<int:doctor_id>', methods=['GET'])
def get_doctor_appointments(doctor_id):
    """Get all appointments for a specific doctor"""
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    return jsonify([a.to_dict() for a in appointments])



# ============================================================================
# Resource Routes
# ============================================================================
resource_bp = Blueprint('resources', __name__)


@resource_bp.route('/', methods=['GET'])
def get_resources():
    """Get all resources"""
    resources = Resource.query.all()
    return jsonify([r.to_dict() for r in resources])


@resource_bp.route('/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    """Get a specific resource by ID"""
    resource = Resource.query.get_or_404(resource_id)
    return jsonify(resource.to_dict())


@resource_bp.route('/', methods=['POST'])
def create_resource():
    """Add a new resource"""
    data = request.json
    resource = Resource(
        resource_type=data['resource_type'],
        resource_name=data['resource_name'],
        total_quantity=data['total_quantity'],
        available_quantity=data['available_quantity'],
        location=data.get('location')
    )
    db.session.add(resource)
    db.session.commit()
    return jsonify(resource.to_dict()), 201


@resource_bp.route('/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    """Update an existing resource"""
    resource = Resource.query.get_or_404(resource_id)
    data = request.json
    resource.resource_type = data.get('resource_type', resource.resource_type)
    resource.resource_name = data.get('resource_name', resource.resource_name)
    resource.total_quantity = data.get('total_quantity', resource.total_quantity)
    resource.available_quantity = data.get('available_quantity', resource.available_quantity)
    resource.location = data.get('location', resource.location)
    db.session.commit()
    return jsonify(resource.to_dict())


@resource_bp.route('/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """Delete a resource"""
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    return jsonify({'message': 'Resource deleted successfully'})


@resource_bp.route('/type/<resource_type>', methods=['GET'])
def get_resources_by_type(resource_type):
    """Get resources by type"""
    resources = Resource.query.filter_by(resource_type=resource_type).all()
    return jsonify([r.to_dict() for r in resources])



# ============================================================================
# AI/ML Routes
# ============================================================================
ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/predict', methods=['POST'])
def predict_patients():
    """Predict patient count for a given date"""
    from ai_model import predict_patient_count
    data = request.json
    target_date = data.get('date')
    prediction = predict_patient_count(target_date)
    return jsonify(prediction)


@ai_bp.route('/train', methods=['POST'])
def train_model():
    """Train the AI/ML prediction model"""
    from ai_model import train_model
    result = train_model()
    return jsonify(result)


@ai_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get all patient statistics"""
    stats = PatientStatistics.query.order_by(PatientStatistics.date).all()
    return jsonify([s.to_dict() for s in stats])


@ai_bp.route('/statistics', methods=['POST'])
def add_statistics():
    """Add patient statistics for training"""
    data = request.json
    stat = PatientStatistics(
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        day_of_week=data['day_of_week'],
        patient_count=data['patient_count']
    )
    db.session.add(stat)
    db.session.commit()
    return jsonify(stat.to_dict()), 201



# ============================================================================
# Admin Routes
# ============================================================================
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard statistics"""
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.filter_by(is_active=True).count()
    total_appointments = Appointment.query.count()
    scheduled_appointments = Appointment.query.filter_by(status='scheduled').count()
    completed_appointments = Appointment.query.filter_by(status='completed').count()
    cancelled_appointments = Appointment.query.filter_by(status='cancelled').count()
    total_resources = Resource.query.count()
    
    return jsonify({
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'scheduled_appointments': scheduled_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'total_resources': total_resources
    })


@admin_bp.route('/recent-appointments', methods=['GET'])
def get_recent_appointments():
    """Get recent appointments"""
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(10).all()
    return jsonify([a.to_dict() for a in appointments])


@admin_bp.route('/resource-usage', methods=['GET'])
def get_resource_usage():
    """Get resource usage statistics"""
    resources = Resource.query.all()
    usage_data = []
    for resource in resources:
        usage_percent = (resource.available_quantity / resource.total_quantity) * 100 if resource.total_quantity > 0 else 0
        usage_data.append({
            'resource_name': resource.resource_name,
            'resource_type': resource.resource_type,
            'total': resource.total_quantity,
            'available': resource.available_quantity,
            'usage_percent': round(usage_percent, 2)
        })
    return jsonify(usage_data)
