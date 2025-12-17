import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime
import random
import os
from functools import wraps
import requests  # Komunikasi dengan ML Server
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# KONFIGURASI ML SERVER (LAPTOP 1)
ML_SERVER_URL = 'http://172.20.10.3'  
ML_SERVER_ENABLED = True  

# SQLAlchemy Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'restapp_db'
}
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def safe_category(val, default="Unknown"):
    """Ensure categorical value is not None, empty, or nan."""
    if val is None or (isinstance(val, float) and np.isnan(val)) or str(val).strip().lower() in ["", "nan", "none"]:
        return default
    return val

def predict_stress_via_ml_server(gender, age, occupation, sleep_duration, sleep_quality, 
                                  bmi_category, systolic_bp, diastolic_bp, heart_rate, 
                                  daily_steps, sleep_disorder):
    """
    Mengirim data ke ML Server (Laptop 1) untuk prediksi
    """
    try:
        payload = {
            'gender': gender,
            'age': age,
            'occupation': occupation,
            'sleep_duration': sleep_duration,
            'sleep_quality': sleep_quality,
            'bmi_category': bmi_category,
            'systolic_bp': systolic_bp,
            'diastolic_bp': diastolic_bp,
            'heart_rate': heart_rate,
            'daily_steps': daily_steps,
            'sleep_disorder': sleep_disorder
        }
        
        print(f"🔄 Sending prediction request to ML Server: {ML_SERVER_URL}/predict")
        print(f"📦 Payload: {payload}")
        
        # Kirim POST request ke ML Server
        response = requests.post(
            f'{ML_SERVER_URL}/predict',
            json=payload,
            timeout=10
        )
        
        print(f"✅ ML Server response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Prediction success: {result['stress_level']} (score: {result.get('stress_score')})")
                return result['stress_level']
            else:
                print(f"❌ ML Server returned error: {result.get('error')}")
        
        # Fallback
        print("⚠️ Using fallback prediction...")
        return predict_stress_fallback(sleep_duration, sleep_quality, systolic_bp, 
                                       diastolic_bp, heart_rate, daily_steps, sleep_disorder)
        
    except requests.exceptions.Timeout:
        print("❌ ML Server timeout - using fallback")
        return predict_stress_fallback(sleep_duration, sleep_quality, systolic_bp, 
                                       diastolic_bp, heart_rate, daily_steps, sleep_disorder)
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Cannot connect to ML Server: {e}")
        print(f"   Make sure ML Server is running at {ML_SERVER_URL}")
        return predict_stress_fallback(sleep_duration, sleep_quality, systolic_bp, 
                                       diastolic_bp, heart_rate, daily_steps, sleep_disorder)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return predict_stress_fallback(sleep_duration, sleep_quality, systolic_bp, 
                                       diastolic_bp, heart_rate, daily_steps, sleep_disorder)

def predict_stress_fallback(sleep_duration, sleep_quality, systolic_bp, 
                            diastolic_bp, heart_rate, daily_steps, sleep_disorder):
   
    print("📊 Using fallback prediction (rule-based)")
    stress_score = 0
    
    if sleep_duration < 6:
        stress_score += 2
    elif sleep_duration < 7:
        stress_score += 1
        
    if sleep_quality < 5:
        stress_score += 2
    elif sleep_quality < 7:
        stress_score += 1
        
    if systolic_bp > 130 or diastolic_bp > 85:
        stress_score += 1
        
    if heart_rate > 80:
        stress_score += 1
        
    if daily_steps < 5000:
        stress_score += 1
        
    if sleep_disorder and sleep_disorder.lower() not in ['none', 'nothing']:
        stress_score += 2
    
    if stress_score >= 5:
        return 'High'
    elif stress_score >= 3:
        return 'Medium'
    else:
        return 'Low'

def predict_stress(gender, age, occupation, sleep_duration, sleep_quality, 
                   bmi_category, systolic_bp, diastolic_bp, heart_rate, 
                   daily_steps, sleep_disorder):

    # Clean inputs
    gender = safe_category(gender, "Other")
    occupation = safe_category(occupation, "Other")
    bmi_category = safe_category(bmi_category, "Normal")
    sleep_disorder = safe_category(sleep_disorder, "None")
    
    # Ensure numeric values
    try:
        age = int(age) if age else 30
        sleep_duration = float(sleep_duration) if sleep_duration else 7.0
        sleep_quality = int(sleep_quality) if sleep_quality else 5
        systolic_bp = int(systolic_bp) if systolic_bp else 120
        diastolic_bp = int(diastolic_bp) if diastolic_bp else 80
        heart_rate = int(heart_rate) if heart_rate else 70
        daily_steps = int(daily_steps) if daily_steps else 5000
    except (ValueError, TypeError) as e:
        print(f"⚠️ Error converting values: {e}")
        return "Error"
    
    # Use ML Server if enabled
    if ML_SERVER_ENABLED:
        return predict_stress_via_ml_server(
            gender, age, occupation, sleep_duration, sleep_quality,
            bmi_category, systolic_bp, diastolic_bp, heart_rate,
            daily_steps, sleep_disorder
        )
    else:
        # Use fallback directly
        return predict_stress_fallback(
            sleep_duration, sleep_quality, systolic_bp,
            diastolic_bp, heart_rate, daily_steps, sleep_disorder
        )

# RECOMMENDATION
def get_recommendation(stress_level, sleep_duration=None, heart_rate=None, steps=None):
    """Enhanced rule-based recommendations"""
    recommendations = {
        'Low': [
            "You're doing great! Keep up with your daily walks and maintain your healthy routine.",
            "Excellent work! Consider trying yoga or meditation to maintain this balance.",
            "Keep it up! Your healthy habits are paying off."
        ],
        'Medium': [
            "Consider taking short breaks throughout the day. A 10-minute meditation can help.",
            "Try the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8.",
            "Take a 15-minute nature walk to reset your mind."
        ],
        'High': [
            "Try a 5-minute breathing exercise. Focus on deep, slow breaths.",
            "Consider speaking with a healthcare professional if stress persists.",
            "Practice progressive muscle relaxation before bed."
        ]
    }
    
    # Specific recommendations
    if sleep_duration and sleep_duration < 6:
        return "You're getting less than 6 hours of sleep. Try to sleep 30 minutes earlier tonight."
    if heart_rate and heart_rate > 85:
        return "Your heart rate is elevated. Try 10 minutes of deep breathing exercises."
    if steps and steps < 5000:
        return "You're below 5000 steps today. Take a 10-minute walk after your next meal."
    
    return random.choice(recommendations.get(stress_level, ["Stay mindful of your health."]))

# DATABASE MODELS 

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(50), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    birthdate = db.Column(db.Date)
    occupation = db.Column(db.String(50))
    bmi_category = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    logs = db.relationship('DailyLog', backref='user', lazy=True)

class DailyLog(db.Model):
    __tablename__ = 'daily_logs'
    log_id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(50), db.ForeignKey('users.username'))
    sleep_duration = db.Column(db.Float)
    sleep_quality = db.Column(db.Integer)
    systolic_bp = db.Column(db.Integer)
    diastolic_bp = db.Column(db.Integer)
    heart_rate = db.Column(db.Integer)
    daily_steps = db.Column(db.Integer)
    sleep_disorder = db.Column(db.String(50))
    stress_level = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def calculate_age(birthdate):
    today = datetime.now()
    if isinstance(birthdate, str):
        try:
            birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        except Exception:
            return 30
    age = today.year - birthdate.year
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age -= 1
    return age

# AUTHENTICATION 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ROUTES 

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        birthdate = request.form.get('birthdate')
        occupation = request.form.get('occupation')
        bmi_category = request.form.get('bmi_category')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                birthdate=birthdate,
                occupation=occupation,
                bmi_category=bmi_category,
                password_hash=password_hash
            )
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    
    stress_level = "Low"
    recommendation_text = "Welcome! Start by adding your first daily log to get personalized recommendations."
    avg_heart_rate = 0
    
    if user:
        latest_log = DailyLog.query.filter_by(username=username).filter(DailyLog.stress_level != None).order_by(DailyLog.timestamp.desc()).first()
        if latest_log:
            stress_level = latest_log.stress_level
            recommendation_text = get_recommendation(
                stress_level=stress_level,
                sleep_duration=latest_log.sleep_duration,
                heart_rate=latest_log.heart_rate,
                steps=latest_log.daily_steps
            )
        avg_hr = db.session.query(db.func.avg(DailyLog.heart_rate)).filter_by(username=username).scalar()
        if avg_hr:
            avg_heart_rate = round(avg_hr)
        return render_template('dashboard.html', 
                             user=user, 
                             stress_level=stress_level, 
                             avg_heart_rate=avg_heart_rate,
                             recommendation=recommendation_text)
    
    return render_template('dashboard.html', 
                         stress_level="Low", 
                         recommendation="Unable to load recommendations.", 
                         avg_heart_rate=0)

@app.route('/add_log', methods=['GET', 'POST'])
@login_required
def add_log():
    if request.method == 'POST':
        username = session['username']

        sleep_duration = float(request.form['sleep_duration'])
        sleep_quality = int(request.form['sleep_quality'])
        systolic_bp = int(request.form['systolic_bp'])
        diastolic_bp = int(request.form['diastolic_bp'])
        heart_rate = int(request.form['heart_rate'])
        daily_steps = int(request.form['daily_steps'])
        sleep_disorder = request.form['sleep_disorder']

        user = User.query.filter_by(username=username).first()
        age = calculate_age(user.birthdate)

        # Predict stress level menggunakan ML Server atau fallback
        print("\n" + "="*50)
        print("🎯 STARTING STRESS PREDICTION")
        print("="*50)
        
        stress_level = predict_stress(
            user.gender,
            age,
            user.occupation,
            sleep_duration,
            sleep_quality,
            user.bmi_category,
            systolic_bp,
            diastolic_bp,
            heart_rate,
            daily_steps,
            sleep_disorder
        )
        
        print(f"📊 Final prediction: {stress_level}")
        print("="*50 + "\n")

        log_id = f"{username}_{datetime.now().strftime('%Y%m%d')}"
        log = DailyLog.query.filter_by(log_id=log_id).first()
        if log:
            log.sleep_duration = sleep_duration
            log.sleep_quality = sleep_quality
            log.systolic_bp = systolic_bp
            log.diastolic_bp = diastolic_bp
            log.heart_rate = heart_rate
            log.daily_steps = daily_steps
            log.sleep_disorder = sleep_disorder
            log.stress_level = stress_level
            log.timestamp = datetime.now()
        else:
            log = DailyLog(
                log_id=log_id,
                username=username,
                sleep_duration=sleep_duration,
                sleep_quality=sleep_quality,
                systolic_bp=systolic_bp,
                diastolic_bp=diastolic_bp,
                heart_rate=heart_rate,
                daily_steps=daily_steps,
                sleep_disorder=sleep_disorder,
                stress_level=stress_level,
                timestamp=datetime.now()
            )
            db.session.add(log)
        db.session.commit()

        flash(f'Daily log added successfully! Predicted stress level: {stress_level}', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_log.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    
    if request.method == 'POST':
        try:
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')
            user.gender = request.form.get('gender')
            user.birthdate = request.form.get('birthdate')
            user.occupation = request.form.get('occupation')
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return render_template('profile.html', user=user)
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
            return render_template('profile.html', user=user)
    
    return render_template('profile.html', user=user)

# API Endpoints

@app.route('/api/steps_data')
@login_required
def get_steps_data():
    username = session['username']
    logs = DailyLog.query.filter_by(username=username).order_by(DailyLog.timestamp.desc()).limit(30).all()
    logs = list(reversed(logs))
    return jsonify({
        'labels': [log.timestamp.strftime('%m/%d') for log in logs],
        'data': [log.daily_steps for log in logs]
    })

@app.route('/api/sleep_data')
@login_required
def get_sleep_data():
    username = session['username']
    logs = DailyLog.query.filter_by(username=username).order_by(DailyLog.timestamp.desc()).limit(7).all()
    logs = list(reversed(logs))
    return jsonify({
        'labels': [log.timestamp.strftime('%m/%d') for log in logs],
        'data': [float(log.sleep_duration) for log in logs]
    })

@app.route('/api/bp_data')
@login_required
def get_bp_data():
    username = session['username']
    logs = DailyLog.query.filter_by(username=username).order_by(DailyLog.timestamp.desc()).limit(7).all()
    logs = list(reversed(logs))
    return jsonify({
        'labels': [log.timestamp.strftime('%m/%d') for log in logs],
        'systolic': [log.systolic_bp for log in logs],
        'diastolic': [log.diastolic_bp for log in logs]
    })

@app.route('/api/ml_server_status')
@login_required
def ml_server_status():
    """Check if ML Server is reachable"""
    try:
        response = requests.get(f'{ML_SERVER_URL}/health', timeout=5)
        if response.status_code == 200:
            return jsonify({
                'status': 'online',
                'message': 'ML Server is running',
                'url': ML_SERVER_URL
            })
    except:
        pass
    
    return jsonify({
        'status': 'offline',
        'message': 'ML Server is not reachable. Using fallback prediction.',
        'url': ML_SERVER_URL
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌐 WEB SERVER - LAPTOP 2 (Flask Application)")
    print("="*70)
    print(f"🔗 ML Server URL: {ML_SERVER_URL}")
    print(f" ML Server Enabled: {ML_SERVER_ENABLED}")
    print(f" Database: {DB_CONFIG['database']} @ {DB_CONFIG['host']}")
    print("\n📋 Server will run on: http://0.0.0.0:5000")
    print("\n IMPORTANT SETUP:")
    print("   1. Make sure ML Server is running on Laptop 1")
    print("   2. Update ML_SERVER_URL with correct IP address")
    print("   3. Both laptops must be on the same network")
    print("   4. Test connection: visit http://<your-ip>:5000/api/ml_server_status")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)