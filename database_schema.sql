-- Hospital Management System Database Schema

CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- Patients Table
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    age INT,
    gender VARCHAR(10),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Doctors Table
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    available_days VARCHAR(50),
    start_time TIME,
    end_time TIME,
    is_active BOOLEAN DEFAULT TRUE
);

-- Appointments Table
CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status ENUM('scheduled', 'completed', 'cancelled') DEFAULT 'scheduled',
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- Resources Table
CREATE TABLE resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    resource_type VARCHAR(50) NOT NULL,
    resource_name VARCHAR(100) NOT NULL,
    total_quantity INT NOT NULL,
    available_quantity INT NOT NULL,
    location VARCHAR(100)
);

-- Patient Statistics (for AI/ML)
CREATE TABLE patient_statistics (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    patient_count INT NOT NULL,
    UNIQUE KEY unique_date (date)
);

-- Insert sample data
INSERT INTO doctors (name, specialization, email, phone, available_days, start_time, end_time) VALUES
('Dr. Smith', 'Cardiology', 'smith@hospital.com', '1234567890', 'Monday,Wednesday,Friday', '09:00:00', '17:00:00'),
('Dr. Johnson', 'Neurology', 'johnson@hospital.com', '0987654321', 'Tuesday,Thursday', '10:00:00', '18:00:00'),
('Dr. Williams', 'Orthopedics', 'williams@hospital.com', '1122334455', 'Monday,Tuesday,Wednesday,Thursday,Friday', '08:00:00', '16:00:00');

INSERT INTO resources (resource_type, resource_name, total_quantity, available_quantity, location) VALUES
('Bed', 'General Ward Bed', 50, 45, 'Ground Floor'),
('Bed', 'ICU Bed', 10, 8, 'First Floor'),
('Equipment', 'X-Ray Machine', 2, 2, 'Basement'),
('Equipment', 'MRI Machine', 1, 1, 'First Floor'),
('Room', 'Operation Theater', 3, 3, 'Second Floor');

-- Insert sample patient statistics for AI/ML training
INSERT INTO patient_statistics (date, day_of_week, patient_count) VALUES
('2024-01-01', 'Monday', 100),
('2024-01-02', 'Tuesday', 60),
('2024-01-03', 'Wednesday', 80),
('2024-01-04', 'Thursday', 70),
('2024-01-05', 'Friday', 90),
('2024-01-06', 'Saturday', 40),
('2024-01-07', 'Sunday', 30),
('2024-01-08', 'Monday', 105),
('2024-01-09', 'Tuesday', 65),
('2024-01-10', 'Wednesday', 85),
('2024-01-11', 'Thursday', 75),
('2024-01-12', 'Friday', 95),
('2024-01-13', 'Saturday', 45),
('2024-01-14', 'Sunday', 35);
