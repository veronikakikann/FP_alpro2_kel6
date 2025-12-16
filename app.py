from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import mysql.connector
from mysql.connector import Error
import bcrypt
from datetime import datetime, timedelta
import random
import pickle
import os
from functools import wraps
import joblib
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'restapp_db'
}

# ML MODEL PLACEHOLDER
# ===== LOAD MODEL =====
import joblib
import pandas as pd

MODEL = None

def load_ml_model():
    global MODEL
    try:
        MODEL = joblib.load('model/stress_predictor_model.pkl')
        print("MODEL STATUS: OK")
    except Exception as e:
        print("MODEL STATUS: FAILED")
        print(e)

load_ml_model()

def predict_stress(
    gender, age, occupation,
    sleep_duration, sleep_quality,
    bmi_category, systolic_bp, diastolic_bp,
    heart_rate, daily_steps, sleep_disorder
):
    if MODEL is None:
        return "Model Not Loaded"

    try:
        input_df = pd.DataFrame([{
            'Gender': gender,
            'Age': int(age),
            'Occupation': occupation,
            'Sleep Duration': float(sleep_duration),
            'Quality of Sleep': int(sleep_quality),
            'BMI Category': bmi_category,
            'Heart Rate': int(heart_rate),
            'Daily Steps': int(daily_steps),
            'Systolic BP': int(systolic_bp),
            'Diastolic BP': int(diastolic_bp),
            'Sleep Disorder': sleep_disorder
        }])

        input_df['BP_Ratio'] = input_df['Diastolic BP'] / input_df['Systolic BP']

        input_df['Age_Group'] = pd.cut(
            input_df['Age'],
            bins=[18, 30, 45, 60, 120],
            labels=['Young', 'Adult', 'Mid-Age', 'Senior']
        )

        prediction = MODEL.predict(input_df)
        return prediction[0]

    except Exception as e:
        print("Prediction error:", e)
        return "Error"

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
    
    # Tambahkan rekomendasi spesifik berdasarkan metrics lain
    if sleep_duration and sleep_duration < 6:
        return "You're getting less than 6 hours of sleep. Try to sleep 30 minutes earlier tonight."
    
    if heart_rate and heart_rate > 85:
        return "Your heart rate is elevated. Try 10 minutes of deep breathing exercises."
    
    if steps and steps < 5000:
        return "You're below 5000 steps today. Take a 10-minute walk after your next meal."
    
    # Random dari list untuk variasi
    import random
    return random.choice(recommendations.get(stress_level, ["Stay mindful of your health."]))

# DATABASE FUNCTIONS

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None
    
def get_user_info(username):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="namadb"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT gender FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def calculate_age(birthdate):
    today = datetime.now()
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
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Check if username exists
                cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    flash('Username already exists', 'error')
                    return render_template('register.html')
                
                # Hash password
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Insert user
                query = """INSERT INTO users (username, first_name, last_name, gender, birthdate, 
                          occupation, bmi_category, password_hash) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (username, first_name, last_name, gender, birthdate, 
                                     occupation, bmi_category, password_hash))
                conn.commit()
                
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
                
            except Error as e:
                flash(f'Registration failed: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                
                if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    session['username'] = username
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid username or password', 'error')
                    
            except Error as e:
                flash(f'Login failed: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    conn = get_db_connection()
    
    # Default values jika user baru/belum ada log
    stress_level = "Low"
    recommendation_text = "Welcome! Start by adding your first daily log to get personalized recommendations."
    avg_heart_rate = 0
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Get user info
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            # 1. PERUBAHAN DISINI: Ambil semua metrics, bukan cuma stress_level
            # Kita butuh sleep, heart_rate, dan steps untuk logika rekomendasi
            cursor.execute("""SELECT stress_level, sleep_duration, heart_rate, daily_steps 
                              FROM daily_logs 
                              WHERE username = %s AND stress_level IS NOT NULL
                              ORDER BY timestamp DESC LIMIT 1""", (username,))
            latest_log = cursor.fetchone()
            
            # 2. Logika memproses data log terakhir
            if latest_log:
                stress_level = latest_log['stress_level']
                
                # PANGGIL FUNGSI REKOMENDASI DISINI
                recommendation_text = get_recommendation(
                    stress_level=stress_level,
                    sleep_duration=latest_log['sleep_duration'],
                    heart_rate=latest_log['heart_rate'],
                    steps=latest_log['daily_steps']
                )
            
            # Get average heart rate
            cursor.execute("""SELECT AVG(heart_rate) as avg_hr FROM daily_logs 
                              WHERE username = %s""", (username,))
            avg_hr = cursor.fetchone()
            if avg_hr and avg_hr['avg_hr']:
                avg_heart_rate = round(avg_hr['avg_hr'])
            
            # 3. Kirim variable 'recommendation' ke HTML
            return render_template('dashboard.html', 
                                 user=user, 
                                 stress_level=stress_level, 
                                 avg_heart_rate=avg_heart_rate,
                                 recommendation=recommendation_text) # <--- Variable baru
                                 
        except Error as e:
            flash(f'Error loading dashboard: {str(e)}', 'error')
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()
    
    # Fallback jika koneksi DB gagal
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

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        age = calculate_age(user['birthdate'])

        stress_level = predict_stress(
            user['gender'],
            age,
            user['occupation'],
            sleep_duration,
            sleep_quality,
            user['bmi_category'],
            systolic_bp,
            diastolic_bp,
            heart_rate,
            daily_steps,
            sleep_disorder
        )

        log_id = f"{username}_{datetime.now().strftime('%Y%m%d')}"

        cursor.execute("""
        INSERT INTO daily_logs (
            log_id, username, sleep_duration, sleep_quality,
            systolic_bp, diastolic_bp, heart_rate,
            daily_steps, sleep_disorder, stress_level
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            sleep_duration=VALUES(sleep_duration),
            sleep_quality=VALUES(sleep_quality),
            systolic_bp=VALUES(systolic_bp),
            diastolic_bp=VALUES(diastolic_bp),
            heart_rate=VALUES(heart_rate),
            daily_steps=VALUES(daily_steps),
            sleep_disorder=VALUES(sleep_disorder),
            stress_level=VALUES(stress_level)
        """, (
            log_id, username, sleep_duration, sleep_quality,
            systolic_bp, diastolic_bp, heart_rate,
            daily_steps, sleep_disorder, stress_level
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('add_log.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = session['username']
    conn = get_db_connection()
    
    if request.method == 'POST':
        if conn:
            try:
                cursor = conn.cursor()
                
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                gender = request.form.get('gender')
                birthdate = request.form.get('birthdate')
                occupation = request.form.get('occupation')
                
                query = """UPDATE users SET first_name=%s, last_name=%s, gender=%s, 
                          birthdate=%s, occupation=%s WHERE username=%s"""
                cursor.execute(query, (first_name, last_name, gender, birthdate, 
                                     occupation, username))
                conn.commit()
                
                flash('Profile updated successfully!', 'success')
                
                # Fetch updated user data
                cursor.close()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                cursor.close()
                conn.close()
                return render_template('profile.html', user=user)
            except Error as e:
                flash(f'Error updating profile: {str(e)}', 'error')
                cursor.close()
                conn.close()
                return render_template('profile.html', user=None)
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            return render_template('profile.html', user=user)
        except Error as e:
            flash(f'Error loading profile: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('profile.html', user=None)

# API endpoints for charts
@app.route('/api/steps_data')
@login_required
def get_steps_data():
    username = session['username']
    conn = get_db_connection()
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """SELECT DATE(timestamp) as date, daily_steps 
                      FROM daily_logs WHERE username = %s 
                      ORDER BY timestamp DESC LIMIT 30"""
            cursor.execute(query, (username,))
            data = cursor.fetchall()
            
            return jsonify({
                'labels': [row['date'].strftime('%m/%d') for row in reversed(data)],
                'data': [row['daily_steps'] for row in reversed(data)]
            })
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    
    return jsonify({'labels': [], 'data': []})

@app.route('/api/sleep_data')
@login_required
def get_sleep_data():
    username = session['username']
    conn = get_db_connection()
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """SELECT DATE(timestamp) as date, sleep_duration 
                      FROM daily_logs WHERE username = %s 
                      ORDER BY timestamp DESC LIMIT 7"""
            cursor.execute(query, (username,))
            data = cursor.fetchall()
            
            return jsonify({
                'labels': [row['date'].strftime('%m/%d') for row in reversed(data)],
                'data': [float(row['sleep_duration']) for row in reversed(data)]
            })
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    
    return jsonify({'labels': [], 'data': []})

@app.route('/api/bp_data')
@login_required
def get_bp_data():
    username = session['username']
    conn = get_db_connection()
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """SELECT DATE(timestamp) as date, systolic_bp, diastolic_bp 
                      FROM daily_logs WHERE username = %s 
                      ORDER BY timestamp DESC LIMIT 7"""
            cursor.execute(query, (username,))
            data = cursor.fetchall()
            
            return jsonify({
                'labels': [row['date'].strftime('%m/%d') for row in reversed(data)],
                'systolic': [row['systolic_bp'] for row in reversed(data)],
                'diastolic': [row['diastolic_bp'] for row in reversed(data)]
            })
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    
    return jsonify({'labels': [], 'systolic': [], 'diastolic': []})

if __name__ == '__main__':

    app.run(debug=True)
