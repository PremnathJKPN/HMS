const API_BASE = '/api';

// Navigation
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
    
    document.querySelectorAll('nav button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

// Patient Sub Navigation
function showPatientSubSection(subSectionId) {
    document.querySelectorAll('#patient-dashboard-section .sub-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(subSectionId).classList.add('active');
    
    document.querySelectorAll('#patient-dashboard-section .sub-nav button').forEach(btn => {
        btn.classList.remove('active');
    });
    if (event && event.target) {
        event.target.classList.add('active');
    }
}

// Hospital Sub Navigation
function showHospitalSubSection(subSectionId) {
    document.querySelectorAll('#hospital-dashboard-section .sub-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(subSectionId).classList.add('active');
    
    document.querySelectorAll('#hospital-dashboard-section .sub-nav button').forEach(btn => {
        btn.classList.remove('active');
    });
    if (event && event.target) {
        event.target.classList.add('active');
    }
}

// API Helper Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API Error:', error);
        return { error: error.message };
    }
}

// Patient Functions
async function loadPatients() {
    const patients = await apiCall('/patients');
    const tbody = document.getElementById('patients-table-body');
    tbody.innerHTML = '';
    
    if (patients.error) {
        tbody.innerHTML = `<tr><td colspan="7" class="alert alert-error">${patients.error}</td></tr>`;
        return;
    }
    
    patients.forEach(patient => {
        tbody.innerHTML += `
            <tr>
                <td>${patient.patient_id}</td>
                <td>${patient.name}</td>
                <td>${patient.email}</td>
                <td>${patient.phone}</td>
                <td>${patient.age || '-'}</td>
                <td>${patient.gender || '-'}</td>
                <td>
                    <button class="btn btn-danger" onclick="deletePatient(${patient.patient_id})">Delete</button>
                </td>
            </tr>
        `;
    });
}

async function addPatient() {
    const data = {
        name: document.getElementById('patient-name').value,
        email: document.getElementById('patient-email').value,
        phone: document.getElementById('patient-phone').value,
        age: document.getElementById('patient-age').value || null,
        gender: document.getElementById('patient-gender').value || null,
        address: document.getElementById('patient-address').value || null
    };
    
    // Validation
    if (!data.name || !data.email || !data.phone) {
        alert('Please fill in all required fields (Name, Email, Phone)');
        return;
    }
    
    const result = await apiCall('/patients/', 'POST', data);
    if (result.error) {
        alert('Error: ' + result.error);
    } else {
        alert('Patient added successfully!');
        document.getElementById('patient-form').reset();
        loadPatients();
        loadPatientsSelect();
    }
}

async function deletePatient(patientId) {
    if (confirm('Are you sure you want to delete this patient?')) {
        const result = await apiCall(`/patients/${patientId}/`, 'DELETE');
        if (result.error) {
            alert('Error: ' + result.error);
        } else {
            alert('Patient deleted successfully!');
            loadPatients();
            loadPatientsSelect();
        }
    }
}

// Doctor Functions
async function loadDoctors() {
    const doctors = await apiCall('/doctors/');
    const tbody = document.getElementById('doctors-table-body');
    tbody.innerHTML = '';
    
    if (doctors.error) {
        tbody.innerHTML = `<tr><td colspan="8" class="alert alert-error">${doctors.error}</td></tr>`;
        return;
    }
    
    doctors.forEach(doctor => {
        tbody.innerHTML += `
            <tr>
                <td>${doctor.doctor_id}</td>
                <td>${doctor.name}</td>
                <td>${doctor.specialization}</td>
                <td>${doctor.email}</td>
                <td>${doctor.phone}</td>
                <td>${doctor.available_days || '-'}</td>
                <td>${doctor.start_time || '-'} - ${doctor.end_time || '-'}</td>
                <td>
                    <button class="btn btn-danger" onclick="deleteDoctor(${doctor.doctor_id})">Delete</button>
                </td>
            </tr>
        `;
    });
}

async function addDoctor() {
    const data = {
        name: document.getElementById('doctor-name').value,
        specialization: document.getElementById('doctor-specialization').value,
        email: document.getElementById('doctor-email').value,
        phone: document.getElementById('doctor-phone').value,
        available_days: document.getElementById('doctor-days').value || null,
        start_time: document.getElementById('doctor-start').value || null,
        end_time: document.getElementById('doctor-end').value || null
    };
    
    // Validation
    if (!data.name || !data.specialization || !data.email || !data.phone) {
        alert('Please fill in all required fields (Name, Specialization, Email, Phone)');
        return;
    }
    
    const result = await apiCall('/doctors/', 'POST', data);
    if (result.error) {
        alert('Error: ' + result.error);
    } else {
        alert('Doctor added successfully!');
        document.getElementById('doctor-form').reset();
        loadDoctors();
        loadDoctorsSelect();
    }
}

async function deleteDoctor(doctorId) {
    if (confirm('Are you sure you want to delete this doctor?')) {
        const result = await apiCall(`/doctors/${doctorId}/`, 'DELETE');
        if (result.error) {
            alert('Error: ' + result.error);
        } else {
            alert('Doctor deleted successfully!');
            loadDoctors();
            loadDoctorsSelect();
        }
    }
}

// Appointment Functions
async function loadAppointments() {
    const appointments = await apiCall('/appointments/');
    const tbody = document.getElementById('appointments-table-body');
    tbody.innerHTML = '';
    
    if (appointments.error) {
        tbody.innerHTML = `<tr><td colspan="7" class="alert alert-error">${appointments.error}</td></tr>`;
        return;
    }
    
    appointments.forEach(appointment => {
        tbody.innerHTML += `
            <tr>
                <td>${appointment.appointment_id}</td>
                <td>${appointment.patient ? appointment.patient.name : 'N/A'}</td>
                <td>${appointment.doctor ? appointment.doctor.name : 'N/A'}</td>
                <td>${appointment.appointment_date}</td>
                <td>${appointment.appointment_time}</td>
                <td>${appointment.status}</td>
                <td>
                    <button class="btn btn-danger" onclick="cancelAppointment(${appointment.appointment_id})">Cancel</button>
                </td>
            </tr>
        `;
    });
}

async function loadDoctorsSelect() {
    const doctors = await apiCall('/doctors/');
    const select = document.getElementById('appointment-doctor');
    select.innerHTML = '<option value="">Select Doctor</option>';
    
    if (!doctors.error) {
        doctors.forEach(doctor => {
            select.innerHTML += `<option value="${doctor.doctor_id}">${doctor.name}</option>`;
        });
    }
}

async function loadPatientsSelect() {
    const patients = await apiCall('/patients/');
    const select = document.getElementById('appointment-patient');
    select.innerHTML = '<option value="">Select Patient</option>';
    
    if (!patients.error) {
        patients.forEach(patient => {
            select.innerHTML += `<option value="${patient.patient_id}">${patient.name}</option>`;
        });
    }
}

async function bookAppointment() {
    const data = {
        patient_id: document.getElementById('appointment-patient').value,
        doctor_id: document.getElementById('appointment-doctor').value,
        appointment_date: document.getElementById('appointment-date').value,
        appointment_time: document.getElementById('appointment-time').value,
        reason: document.getElementById('appointment-reason').value || null
    };
    
    // Validation
    if (!data.patient_id || !data.doctor_id || !data.appointment_date || !data.appointment_time) {
        alert('Please fill in all required fields (Patient, Doctor, Date, Time)');
        return;
    }
    
    const result = await apiCall('/appointments/', 'POST', data);
    if (result.error) {
        alert('Error: ' + result.error);
    } else {
        alert('Appointment booked successfully!');
        document.getElementById('appointment-form').reset();
        loadAppointments();
    }
}

async function cancelAppointment(appointmentId) {
    if (confirm('Are you sure you want to cancel this appointment?')) {
        const result = await apiCall(`/appointments/${appointmentId}/`, 'DELETE');
        if (result.error) {
            alert('Error: ' + result.error);
        } else {
            alert('Appointment cancelled successfully!');
            loadAppointments();
        }
    }
}

// Resource Functions
async function loadResources() {
    const resources = await apiCall('/resources/');
    const tbody = document.getElementById('resources-table-body');
    tbody.innerHTML = '';
    
    if (resources.error) {
        tbody.innerHTML = `<tr><td colspan="6" class="alert alert-error">${resources.error}</td></tr>`;
        return;
    }
    
    resources.forEach(resource => {
        tbody.innerHTML += `
            <tr>
                <td>${resource.resource_id}</td>
                <td>${resource.resource_type}</td>
                <td>${resource.resource_name}</td>
                <td>${resource.total_quantity}</td>
                <td>${resource.available_quantity}</td>
                <td>${resource.location || '-'}</td>
            </tr>
        `;
    });
}

// AI/ML Functions
async function predictPatients() {
    const date = document.getElementById('prediction-date').value;
    if (!date) {
        alert('Please select a date');
        return;
    }
    
    const result = await apiCall('/ai/predict', 'POST', { date });
    const predictionBox = document.getElementById('prediction-result');
    
    if (result.error) {
        predictionBox.innerHTML = `<div class="alert alert-error">${result.error}</div>`;
    } else {
        predictionBox.innerHTML = `
            <div class="prediction-item">
                <strong>Date:</strong> ${result.date} (${result.day_of_week})
            </div>
            <div class="prediction-item">
                <strong>Predicted Patients:</strong> ${result.predicted_patients}
            </div>
            <div class="prediction-item">
                <strong>Historical Average:</strong> ${result.historical_average}
            </div>
            <div class="prediction-item">
                <strong>Recommendation:</strong> ${result.recommendation}
            </div>
        `;
    }
}

async function trainModel() {
    const result = await apiCall('/ai/train', 'POST');
    if (result.error) {
        alert('Error: ' + result.error);
    } else {
        alert(`Model trained successfully!\nMAE: ${result.mae}\nRMSE: ${result.rmse}`);
    }
}

// Admin Dashboard Functions
async function loadDashboard() {
    const dashboard = await apiCall('/admin/dashboard');
    
    if (dashboard.error) {
        console.error(dashboard.error);
        return;
    }
    
    // Patient Dashboard
    document.getElementById('total-patients').textContent = dashboard.total_patients;
    document.getElementById('scheduled-appointments').textContent = dashboard.scheduled_appointments;
    
    // Hospital Dashboard
    document.getElementById('total-patients-hospital').textContent = dashboard.total_patients;
    document.getElementById('total-doctors-hospital').textContent = dashboard.total_doctors;
    document.getElementById('total-appointments-hospital').textContent = dashboard.total_appointments;
    document.getElementById('scheduled-appointments-hospital').textContent = dashboard.scheduled_appointments;
    document.getElementById('completed-appointments-hospital').textContent = dashboard.completed_appointments;
    document.getElementById('cancelled-appointments-hospital').textContent = dashboard.cancelled_appointments;
    document.getElementById('total-resources-hospital').textContent = dashboard.total_resources;
}

async function loadResourceUsage() {
    const usage = await apiCall('/admin/resource-usage');
    const container = document.getElementById('resource-usage-container');
    container.innerHTML = '';
    
    if (usage.error) {
        container.innerHTML = `<div class="alert alert-error">${usage.error}</div>`;
        return;
    }
    
    usage.forEach(item => {
        const color = item.usage_percent < 30 ? '#e74c3c' : item.usage_percent < 70 ? '#f39c12' : '#27ae60';
        container.innerHTML += `
            <div class="card">
                <h3>${item.resource_name}</h3>
                <p><strong>Type:</strong> ${item.resource_type}</p>
                <p><strong>Available:</strong> ${item.available} / ${item.total}</p>
                <div style="background: #ddd; height: 20px; border-radius: 10px; margin-top: 10px;">
                    <div style="background: ${color}; height: 100%; width: ${item.usage_percent}%; border-radius: 10px;"></div>
                </div>
                <p><strong>Usage:</strong> ${item.usage_percent}%</p>
            </div>
        `;
    });
}

// Modal Functions
async function showDetailModal(type, statusFilter = null) {
    const modal = document.getElementById('detail-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalContent = document.getElementById('modal-content');
    
    modal.style.display = 'block';
    modalContent.innerHTML = '<div class="loading">Loading...</div>';
    
    let data;
    let title;
    let tableHTML;
    
    switch(type) {
        case 'patients':
            title = 'All Patients';
            data = await apiCall('/patients/');
            tableHTML = generatePatientTable(data);
            break;
        case 'doctors':
            title = 'All Doctors';
            data = await apiCall('/doctors/');
            tableHTML = generateDoctorTable(data);
            break;
        case 'appointments':
            if (statusFilter) {
                title = `${statusFilter.charAt(0).toUpperCase() + statusFilter.slice(1)} Appointments`;
                data = await apiCall('/appointments/');
                if (!data.error) {
                    data = data.filter(app => app.status === statusFilter);
                }
            } else {
                title = 'All Appointments';
                data = await apiCall('/appointments/');
            }
            tableHTML = generateAppointmentTable(data);
            break;
        case 'resources':
            title = 'All Resources';
            data = await apiCall('/resources/');
            tableHTML = generateResourceTable(data);
            break;
    }
    
    modalTitle.textContent = title;
    modalContent.innerHTML = tableHTML;
}

function closeModal() {
    document.getElementById('detail-modal').style.display = 'none';
}

function generatePatientTable(patients) {
    if (patients.error) {
        return `<div class="alert alert-error">${patients.error}</div>`;
    }
    
    if (patients.length === 0) {
        return '<p>No patients found.</p>';
    }
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Age</th>
                    <th>Gender</th>
                    <th>Address</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    patients.forEach(patient => {
        html += `
            <tr>
                <td>${patient.patient_id}</td>
                <td>${patient.name}</td>
                <td>${patient.email}</td>
                <td>${patient.phone}</td>
                <td>${patient.age || '-'}</td>
                <td>${patient.gender || '-'}</td>
                <td>${patient.address || '-'}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    return html;
}

function generateDoctorTable(doctors) {
    if (doctors.error) {
        return `<div class="alert alert-error">${doctors.error}</div>`;
    }
    
    if (doctors.length === 0) {
        return '<p>No doctors found.</p>';
    }
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Specialization</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Available Days</th>
                    <th>Working Hours</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    doctors.forEach(doctor => {
        html += `
            <tr>
                <td>${doctor.doctor_id}</td>
                <td>${doctor.name}</td>
                <td>${doctor.specialization}</td>
                <td>${doctor.email}</td>
                <td>${doctor.phone}</td>
                <td>${doctor.available_days || '-'}</td>
                <td>${doctor.start_time || '-'} - ${doctor.end_time || '-'}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    return html;
}

function generateAppointmentTable(appointments) {
    if (appointments.error) {
        return `<div class="alert alert-error">${appointments.error}</div>`;
    }
    
    if (appointments.length === 0) {
        return '<p>No appointments found.</p>';
    }
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Patient</th>
                    <th>Doctor</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Status</th>
                    <th>Reason</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    appointments.forEach(appointment => {
        html += `
            <tr>
                <td>${appointment.appointment_id}</td>
                <td>${appointment.patient ? appointment.patient.name : 'N/A'}</td>
                <td>${appointment.doctor ? appointment.doctor.name : 'N/A'}</td>
                <td>${appointment.appointment_date}</td>
                <td>${appointment.appointment_time}</td>
                <td><span class="status-${appointment.status}">${appointment.status}</span></td>
                <td>${appointment.reason || '-'}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    return html;
}

function generateResourceTable(resources) {
    if (resources.error) {
        return `<div class="alert alert-error">${resources.error}</div>`;
    }
    
    if (resources.length === 0) {
        return '<p>No resources found.</p>';
    }
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Name</th>
                    <th>Total</th>
                    <th>Available</th>
                    <th>Location</th>
                    <th>Usage %</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    resources.forEach(resource => {
        const usagePercent = resource.total_quantity > 0 
            ? ((resource.available_quantity / resource.total_quantity) * 100).toFixed(2)
            : 0;
        
        html += `
            <tr>
                <td>${resource.resource_id}</td>
                <td>${resource.resource_type}</td>
                <td>${resource.resource_name}</td>
                <td>${resource.total_quantity}</td>
                <td>${resource.available_quantity}</td>
                <td>${resource.location || '-'}</td>
                <td>${usagePercent}%</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    return html;
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('detail-modal');
    if (event.target == modal) {
        closeModal();
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadPatients();
    loadDoctors();
    loadAppointments();
    loadResources();
    loadDashboard();
    loadResourceUsage();
    loadDoctorsSelect();
    loadPatientsSelect();
});
