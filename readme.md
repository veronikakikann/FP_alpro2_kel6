# REST App - Real-time Evaluation of Stress & Tension

A beautiful web application for monitoring user health patterns and predicting stress levels using Machine Learning.

## 🎨 Design Features

- **Soft UI / Glassmorphism** aesthetic with calming gradients
- **Fully Responsive** for mobile and desktop
- **Smooth Animations** with CSS transitions
- **Stress-free Color Palette** (soft mint, sky blue, sage green, peach)
- **Clean Typography** using Nunito font

## 🛠️ Tech Stack

- **Backend:** Python Flask
- **Database:** MySQL
- **Frontend:** HTML5, CSS
- **ML:** Pickle (for model loading)

## 📁 Project Structure

```
rest-app/
├── app.py                  # Flask backend
├── schema.sql              # Database schema
├── requirements.txt        # Python dependencies
├── static/
│   └── css/
│       └── style.css       # Custom styling
└── templates/
    ├── base.html           # Base template
    ├── index.html          # Landing page
    ├── register.html       # Registration
    ├── login.html          # Login
    ├── dashboard.html      # Main dashboard
    ├── add_log.html        # Add daily log
    └── profile.html        # User profile
```

## 🚀 Installation & Setup

### 1. Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

### 2. Clone or Download

Save all the provided files in the project structure above.

### 3. Install Python Dependencies

Create a `requirements.txt` file:

```txt
Flask==2.3.3
mysql-connector-python==8.1.0
bcrypt==4.0.1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database

1. Start MySQL server
2. Create the database:

```bash
mysql -u root -p < schema.sql
```

Or manually in MySQL:

```sql
source schema.sql
```

3. Update database credentials in `app.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD',  # Change this!
    'database': 'restapp_db'
}
```

### 5. Setup Secret Key

In `app.py`, change the secret key:

```python
app.secret_key = 'your_secure_random_key_here'
```

Generate a secure key using Python:

```python
import secrets
print(secrets.token_hex(32))
```

### 6. Run the Application

```bash
python app.py
```

The app will run on `http://127.0.0.1:5000/`

## 🤖 Machine Learning Model Integration

### Current Status

The app includes a **mock prediction function** that uses simple heuristics to determine stress levels. This allows you to test the full application flow.

### How to Add Your Model

1. Place your trained model files in the project root:
   - `model.pkl` - Your trained ML model
   - `scaler.pkl` - Your feature scaler

2. In `app.py`, uncomment these lines in `load_ml_model()`:

```python
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
return model, scaler
```

3. Update the `predict_stress()` function to use your actual model:

```python
def predict_stress(gender, age, occupation, sleep_duration, sleep_quality, 
                   bmi_category, systolic_bp, diastolic_bp, heart_rate, 
                   daily_steps, sleep_disorder):
    
    # Encode categorical variables
    # Create feature array
    # Scale features
    # Make prediction
    # Return stress level
    
    features = prepare_features(...)  # Implement based on your model
    scaled_features = SCALER.transform([features])
    prediction = MODEL.predict(scaled_features)
    
    # Map prediction to Low/Medium/High
    return map_prediction(prediction)
```

## 📊 Database Schema

### Users Table
- `username` (Primary Key)
- `profile_picture`
- `first_name`, `last_name`
- `gender` (M/F)
- `birthdate`
- `occupation`
- `bmi_category` (Normal/Overweight/Obese)
- `password_hash`

### Daily Logs Table
- `log_id` (Primary Key)
- `username` (Foreign Key)
- `timestamp`
- `sleep_duration`, `sleep_quality`
- `systolic_bp`, `diastolic_bp`
- `heart_rate`
- `daily_steps`
- `sleep_disorder` (None/Insomnia/Apnea)
- `stress_level` (Low/Medium/High)

## 🎯 Features

### ✅ Completed
- User registration and authentication
- Secure password hashing with bcrypt
- Dashboard with stress level display
- Interactive charts (Chart.js):
  - Sleep duration (7 days)
  - Daily steps trend (30 days)
  - Blood pressure monitoring (7 days)
- Add daily health logs
- User profile management
- Responsive design
- Glassmorphism UI

### 📝 User Flow

1. **Landing Page** → Learn about the app
2. **Register** → Create account with health info
3. **Login** → Secure authentication
4. **Dashboard** → View stress level and health trends
5. **Add Log** → Input daily health metrics
6. **Profile** → Update personal information

## 🎨 Color Palette

- **Primary Blue:** `#2c3e50` (Text, accents)
- **Soft Mint:** `#a8dadc` (Cards, gradients)
- **Soft Sky:** `#7fb3d5` (Buttons, highlights)
- **Soft Sage:** `#b8d4c4` (Success states)
- **Soft Peach:** `#f1c6b0` (Warm accents)
- **Soft Cream:** `#f8f4e8` (Backgrounds)

## 🔐 Security Features

- Password hashing with bcrypt
- Session-based authentication
- SQL injection prevention (parameterized queries)
- Input validation on client and server side

## 📱 Responsive Breakpoints

- Desktop: > 768px
- Mobile: ≤ 768px

## 🐛 Troubleshooting

### Database Connection Error
- Check MySQL is running
- Verify credentials in `DB_CONFIG`
- Ensure database `restapp_db` exists

### Module Not Found
- Install all dependencies: `pip install -r requirements.txt`

### Charts Not Displaying
- Check browser console for JavaScript errors
- Ensure Chart.js CDN is accessible
- Verify API endpoints return data

## 📈 Future Enhancements

- [ ] Profile picture upload
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Export data as CSV/PDF
- [ ] Health recommendations based on stress level
- [ ] Push notifications
- [ ] Social features (share progress)

## 👥 Default Account

A default admin account is created:
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Important:** Change this password in production!

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Support

For issues or questions, please check:
1. Database connection settings
2. Python dependencies installed
3. MySQL server running
4. Correct file structure

---


**Built with ❤️ using Flask, MySQL, and modern web design principles**
