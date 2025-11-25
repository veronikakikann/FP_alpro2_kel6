from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import mysql.connector
from mysql.connector import Error
import bcrypt
from datetime import datetime, timedelta
import random
import pickle
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'restapp_db'
}

# ======================
# ML MODEL PLACEHOLDER
# ======================
def load_ml_model():
    """
    Load the pre-trained ML model and scaler.
    TODO: Replace this with actual model loading once model.pkl is provided
    """
    # Uncomment these lines when you have the model files:
    # with open('model.pkl', 'rb') as f:
    #     model = pickle.load(f)
    # with open('scaler.pkl', 'rb') as f:
    #     scaler = pickle.load(f)
    # return model, scaler
    return None, None

MODEL, SCALER = load_ml_model()

def predict_stress(gender, age, occupation, sleep_duration, sleep_quality, 
                   bmi_category, systolic_bp, diastolic_bp, heart_rate, 
                   daily_steps, sleep_disorder):
    """
    Predict stress level based on user inputs.
    
    Args:
        gender: 'M' or 'F'
        age: integer (calculated from birthdate)
        occupation: string
        sleep_duration: float (hours)
        sleep_quality: int (1-10)
        bmi_category: 'Normal', 'Overweight', 'Obese'
        systolic_bp: int
        diastolic_bp: int
        heart_rate: int
        daily_steps: int
        sleep_disorder: 'Apnea', 'Insomnia', 'None'
    
    Returns:
        stress_level: 'Low', 'Medium', 'High'
    """
    
    # TODO: When model.pkl and scaler.pkl are available, implement actual prediction:
    # 
    # 1. Encode categorical variables (gender, occupation, bmi_category, sleep_disorder)
    # 2. Create feature array in the correct order
    # 3. Scale features using the loaded scaler
    # 4. Make prediction using the loaded model
    # 5. Map prediction to stress levels (Low/Medium/High)
    #
    # Example:
    # features = prepare_features(gender, age, occupation, sleep_duration, sleep_quality,
    #                            bmi_category, systolic_bp, diastolic_bp, heart_rate,
    #                            daily_steps, sleep_disorder)
    # scaled_features = SCALER.transform([features])
    # prediction = MODEL.predict(scaled_features)
    # stress_level = map_prediction_to_level(prediction)
    
    # MOCK PREDICTION (Replace this when model is available)
    # Simple heuristic for demonstration
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
        
    if sleep_disorder != 'None':
        stress_score += 2
    
    # Map score to stress level
    if stress_score >= 5:
        return 'High'
    elif stress_score >= 3:
        return 'Medium'
    else:
        return 'Low'

# ======================
# DATABASE FUNCTIONS
# ======================
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def calculate_age(birthdate):
    today = datetime.now()
    age = today.year - birthdate.year
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age -= 1
    return age

# ======================
# AUTHENTICATION
# ======================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ======================
# ROUTES
# ======================
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
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Get user info
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            # Get latest stress level
            cursor.execute("""SELECT stress_level FROM daily_logs 
                            WHERE username = %s AND stress_level IS NOT NULL
                            ORDER BY timestamp DESC LIMIT 1""", (username,))
            latest_log = cursor.fetchone()
            stress_level = latest_log['stress_level'] if latest_log else None
            
            # Get average heart rate
            cursor.execute("""SELECT AVG(heart_rate) as avg_hr FROM daily_logs 
                            WHERE username = %s""", (username,))
            avg_hr = cursor.fetchone()
            avg_heart_rate = round(avg_hr['avg_hr']) if avg_hr['avg_hr'] else 0
            
            return render_template('dashboard.html', user=user, stress_level=stress_level, 
                                 avg_heart_rate=avg_heart_rate)
                                 
        except Error as e:
            flash(f'Error loading dashboard: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('dashboard.html')

@app.route('/add_log', methods=['GET', 'POST'])
@login_required
def add_log():
    if request.method == 'POST':
        username = session['username']
        sleep_duration = float(request.form.get('sleep_duration'))
        sleep_quality = int(request.form.get('sleep_quality'))
        systolic_bp = int(request.form.get('systolic_bp'))
        diastolic_bp = int(request.form.get('diastolic_bp'))
        heart_rate = int(request.form.get('heart_rate'))
        daily_steps = int(request.form.get('daily_steps'))
        sleep_disorder = request.form.get('sleep_disorder')
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                
                # Get user details for prediction
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                
                # Calculate age
                age = calculate_age(user['birthdate'])
                
                # Predict stress level
                stress_level = predict_stress(
                    user['gender'], age, user['occupation'],
                    sleep_duration, sleep_quality, user['bmi_category'],
                    systolic_bp, diastolic_bp, heart_rate,
                    daily_steps, sleep_disorder
                )
                
                # Generate unique log_id
                log_id = f"{username}_{datetime.now().strftime('%Y%m%d')}"
                
                # Insert or update log
                query = """
                INSERT INTO daily_logs (log_id, username, sleep_duration, sleep_quality,
                    systolic_bp, diastolic_bp, heart_rate, daily_steps, sleep_disorder, stress_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    sleep_duration=VALUES(sleep_duration),
                    sleep_quality=VALUES(sleep_quality),
                    systolic_bp=VALUES(systolic_bp),
                    diastolic_bp=VALUES(diastolic_bp),
                    heart_rate=VALUES(heart_rate),
                    daily_steps=VALUES(daily_steps),
                    sleep_disorder=VALUES(sleep_disorder),
                    stress_level=VALUES(stress_level)
                """
                cursor.execute(query, (log_id, username, sleep_duration, sleep_quality,
                                     systolic_bp, diastolic_bp, heart_rate, daily_steps,
                                     sleep_disorder, stress_level))
                conn.commit()
                
                flash('Daily log added successfully!', 'success')
                return redirect(url_for('dashboard'))
                
            except Error as e:
                flash(f'Error adding log: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
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