# Hospital Appointment and Resource Optimization Intelligence System

A smart hospital management system that manages appointments and uses AI/ML to predict patient demand and optimize hospital resources.

## Features

- **Patient Module**: Register patients and manage their information
- **Doctor Module**: Manage doctor schedules and availability
- **Appointment Module**: Book, view, and cancel appointments
- **Resource Module**: Monitor beds, equipment, and other hospital resources
- **AI/ML Module**: Predict patient count using historical data
- **Admin Dashboard**: View comprehensive statistics and resource usage

## Technologies

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Database**: SQLite (for easy setup) - Can be switched to MySQL
- **AI/ML**: Python, Pandas, Scikit-learn (Random Forest Regressor)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Navigate to Project Directory

```bash
cd "Hospital Appointment and Resource Optimization Intelligence System"
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

**Note**: The application uses SQLite by default for easy setup. The database will be created automatically with sample data on first run.

## Usage

### Access the Web Interface

Open your browser and navigate to:
```
http://localhost:5000
```

### First Run

On the first run, the application will:
1. Create a SQLite database (`hospital.db`)
2. Initialize all tables
3. Load sample data (3 doctors, 5 resources, 14 days of patient statistics)
4. Start the Flask server on port 5000

### API Endpoints

#### Patients
- `GET /api/patients` - Get all patients
- `POST /api/patients` - Create a new patient
- `GET /api/patients/<id>` - Get a specific patient
- `PUT /api/patients/<id>` - Update patient information
- `DELETE /api/patients/<id>` - Delete a patient

#### Doctors
- `GET /api/doctors` - Get all doctors
- `POST /api/doctors` - Create a new doctor
- `GET /api/doctors/<id>` - Get a specific doctor
- `PUT /api/doctors/<id>` - Update doctor information
- `DELETE /api/doctors/<id>` - Deactivate a doctor

#### Appointments
- `GET /api/appointments` - Get all appointments
- `POST /api/appointments` - Book a new appointment
- `GET /api/appointments/<id>` - Get a specific appointment
- `PUT /api/appointments/<id>` - Update appointment
- `DELETE /api/appointments/<id>` - Cancel an appointment
- `GET /api/appointments/patient/<id>` - Get appointments by patient
- `GET /api/appointments/doctor/<id>` - Get appointments by doctor

#### Resources
- `GET /api/resources` - Get all resources
- `POST /api/resources` - Add a new resource
- `GET /api/resources/<id>` - Get a specific resource
- `PUT /api/resources/<id>` - Update resource
- `DELETE /api/resources/<id>` - Delete a resource
- `GET /api/resources/type/<type>` - Get resources by type

#### AI/ML
- `POST /api/ai/predict` - Predict patient count for a date
  - Body: `{"date": "YYYY-MM-DD"}`
- `POST /api/ai/train` - Train the prediction model
- `GET /api/ai/statistics` - Get historical patient statistics
- `POST /api/ai/statistics` - Add patient statistics

#### Admin
- `GET /api/admin/dashboard` - Get dashboard statistics
- `GET /api/admin/recent-appointments` - Get recent appointments
- `GET /api/admin/resource-usage` - Get resource usage data

## AI/ML Prediction System

The system uses a Random Forest Regressor to predict patient count based on:
- Day of the week
- Day of the month
- Month
- Year

### How to Use

1. Navigate to the "AI Prediction" section in the web interface
2. Select a date
3. Click "Predict" to see the predicted patient count
4. The system provides recommendations for resource allocation

### Training the Model

The model is automatically trained when:
- No trained model exists
- You manually click "Train Model" in the AI section

The system requires at least 7 days of historical data to train effectively.

## Project Structure

```
.
├── app.py                      # Main Flask application
├── models.py                   # SQLAlchemy database models
├── routes.py                   # API route handlers
├── ai_model.py                 # AI/ML prediction model
├── requirements.txt            # Python dependencies
├── database_schema.sql         # MySQL database schema (optional)
├── .env                        # Environment variables
├── hospital.db                 # SQLite database (auto-created)
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css          # Stylesheet
│   └── js/
│       └── app.js             # Frontend JavaScript
└── README.md                  # This file
```

## One-Line Explanation for Viva

"Our project is a smart hospital system that manages appointments and uses AI/ML to predict patient demand and optimize hospital resources."

## Troubleshooting

### Import Errors

If you get import errors:
```bash
pip install -r requirements.txt
```

### Model Training Error

If the model fails to train:
1. Ensure you have at least 7 days of patient statistics in the database
2. The application loads sample data automatically on first run
3. Add more data using the `/api/ai/statistics` endpoint

### Switching to MySQL (Optional)

If you prefer to use MySQL instead of SQLite:
1. Install MySQL Server
2. Create the database using `database_schema.sql`
3. Update `.env` file with MySQL credentials
4. Change the database URI in `app.py` from `sqlite:///hospital.db` to:
   ```python
   f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
   ```

## License

This project is for educational purposes.
