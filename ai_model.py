"""
AI/ML Prediction Model for Patient Count
Uses Random Forest Regressor to predict patient volume
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os
from datetime import datetime
from models import db, PatientStatistics

# Model file paths
MODEL_PATH = 'patient_prediction_model.pkl'
LE_PATH = 'day_encoder.pkl'



def get_training_data():
    """
    Fetch historical patient statistics from database
    
    Returns:
        pd.DataFrame: DataFrame containing date, day_of_week, and patient_count
    """
    stats = PatientStatistics.query.order_by(PatientStatistics.date).all()
    data = []
    for stat in stats:
        data.append({
            'date': stat.date,
            'day_of_week': stat.day_of_week,
            'patient_count': stat.patient_count
        })
    return pd.DataFrame(data)


def prepare_data(df):
    """
    Prepare data for training by extracting features
    
    Args:
        df (pd.DataFrame): Raw data with date column
        
    Returns:
        tuple: (X, y, label_encoder) - Features, target, and encoder
    """
    df = df.copy()
    
    # Extract features from date
    df['day_of_month'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    
    # Encode day of week
    le = LabelEncoder()
    df['day_encoded'] = le.fit_transform(df['day_of_week'])
    
    # Features and target
    features = ['day_encoded', 'day_of_month', 'month', 'year']
    X = df[features]
    y = df['patient_count']
    
    return X, y, le



def train_model():
    """
    Train the prediction model using Random Forest Regressor
    
    Returns:
        dict: Training result with status, metrics, and message
    """
    try:
        # Get data from database
        df = get_training_data()
        
        if len(df) < 7:
            return {
                'status': 'error',
                'message': 'Insufficient data for training. Need at least 7 days of data.'
            }
        
        # Convert date column
        df['date'] = pd.to_datetime(df['date'])
        
        # Prepare data
        X, y, le = prepare_data(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Save model and encoder
        joblib.dump(model, MODEL_PATH)
        joblib.dump(le, LE_PATH)
        
        return {
            'status': 'success',
            'message': 'Model trained successfully',
            'mae': round(mae, 2),
            'rmse': round(rmse, 2),
            'training_samples': len(df)
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }



def predict_patient_count(target_date=None):
    """
    Predict patient count for a given date
    
    Args:
        target_date (str): Date string in format 'YYYY-MM-DD'. If None, uses today.
        
    Returns:
        dict: Prediction result with status, predicted count, and recommendations
    """
    try:
        # Load model and encoder
        if not os.path.exists(MODEL_PATH) or not os.path.exists(LE_PATH):
            # Train model if not exists
            train_result = train_model()
            if train_result['status'] == 'error':
                return train_result
        
        model = joblib.load(MODEL_PATH)
        le = joblib.load(LE_PATH)
        
        # Parse target date
        if target_date:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        else:
            target_date = datetime.now().date()
        
        # Get day of week
        day_of_week = target_date.strftime('%A')
        
        # Prepare features
        day_encoded = le.transform([day_of_week])[0]
        day_of_month = target_date.day
        month = target_date.month
        year = target_date.year
        
        # Create feature array
        features = np.array([[day_encoded, day_of_month, month, year]])
        
        # Predict
        prediction = model.predict(features)[0]
        prediction = max(0, round(prediction))
        
        # Get historical average for comparison
        df = get_training_data()
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            historical_avg = df[df['day_of_week'] == day_of_week]['patient_count'].mean()
            if pd.isna(historical_avg):
                historical_avg = df['patient_count'].mean()
        else:
            historical_avg = 0
        
        return {
            'status': 'success',
            'date': target_date.isoformat(),
            'day_of_week': day_of_week,
            'predicted_patients': prediction,
            'historical_average': round(historical_avg) if not pd.isna(historical_avg) else 0,
            'recommendation': generate_recommendation(prediction, historical_avg)
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }



def generate_recommendation(predicted, historical):
    """
    Generate resource allocation recommendations based on prediction
    
    Args:
        predicted (int): Predicted patient count
        historical (int): Historical average patient count
        
    Returns:
        str: Recommendation message
    """
    if predicted > historical * 1.2:
        return 'High patient volume expected. Increase doctor availability and prepare additional beds.'
    elif predicted < historical * 0.8:
        return 'Low patient volume expected. Optimize resource allocation accordingly.'
    else:
        return 'Normal patient volume expected. Maintain current resource levels.'


def get_weekly_predictions():
    """
    Get predictions for the next 7 days
    
    Returns:
        list: List of prediction dictionaries for each day
    """
    predictions = []
    from datetime import timedelta
    
    for i in range(7):
        future_date = datetime.now() + timedelta(days=i)
        prediction = predict_patient_count(future_date.strftime('%Y-%m-%d'))
        if prediction['status'] == 'success':
            predictions.append(prediction)
    
    return predictions
