import random
from datetime import datetime, timedelta

# Configuration
start_date = datetime(2025, 11, 19)
username = "player"
n_rows = 30
rows = []

for i in range(n_rows):
    # Go backwards in time
    curr_date = start_date - timedelta(days=i)
    timestamp = curr_date.strftime('%Y-%m-%d')
    log_id = f"{username}_{curr_date.strftime('%Y%m%d')}"
    
    # Simulate realistic correlations
    # Randomly decide if today is a "Good", "Okay", or "Bad" health day
    day_type = random.choices(['Good', 'Okay', 'Bad'], weights=[0.5, 0.3, 0.2])[0]
    
    if day_type == 'Good':
        sleep_dur = round(random.uniform(7.5, 9.0), 2)
        sleep_qual = random.randint(8, 10)
        sys_bp = random.randint(110, 120)
        dia_bp = random.randint(70, 80)
        hr = random.randint(60, 75)
        steps = random.randint(8000, 12000)
        disorder = 'None'
        stress = 'Low'
    elif day_type == 'Okay':
        sleep_dur = round(random.uniform(6.0, 7.4), 2)
        sleep_qual = random.randint(5, 7)
        sys_bp = random.randint(121, 129)
        dia_bp = random.randint(81, 85)
        hr = random.randint(76, 85)
        steps = random.randint(5000, 7900)
        disorder = 'None'
        stress = 'Medium'
    else: # Bad day
        sleep_dur = round(random.uniform(4.0, 5.9), 2)
        sleep_qual = random.randint(3, 5)
        sys_bp = random.randint(130, 145)
        dia_bp = random.randint(86, 95)
        hr = random.randint(86, 100)
        steps = random.randint(2000, 4900)
        disorder = random.choice(['Insomnia', 'Apnea'])
        stress = 'High'

    row = f"('{log_id}', '{username}', '{timestamp}', {sleep_dur}, {sleep_qual}, {sys_bp}, {dia_bp}, {hr}, {steps}, '{disorder}', '{stress}')"
    rows.append(row)

# Print formatted SQL
print("INSERT INTO daily_logs (log_id, username, timestamp, sleep_duration, sleep_quality, systolic_bp, diastolic_bp, heart_rate, daily_steps, sleep_disorder, stress_level) VALUES")
print(",\n".join(rows) + ";")