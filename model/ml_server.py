from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Biar bisa diakses dari laptop lain

# Load model saat server start
print("Loading ML model...")
try:
    model = joblib.load('stress_predictor.pkl')
    preprocessor = joblib.load('preprocessor.pkl')
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    model = None
    preprocessor = None

@app.route('/health', methods=['GET'])
def health_check():
    """Check kalau server hidup"""
    return jsonify({
        'status': 'ML Server is running',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict_stress():
    """Endpoint untuk prediksi stress level"""
    try:
        # Terima data dari laptop 2
        data = request.get_json()
        
        # Validasi model
        if model is None or preprocessor is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded'
            }), 500
        
        # Prepare input data
        input_data = {
            'Gender': data['gender'],
            'Age': int(data['age']),
            'Occupation': data['occupation'],
            'Sleep Duration': float(data['sleep_duration']),
            'Quality of Sleep': int(data['sleep_quality']),
            'BMI Category': data['bmi_category'],
            'Heart Rate': int(data['heart_rate']),
            'Daily Steps': int(data['daily_steps']),
            'Systolic BP': int(data['systolic_bp']),
            'Diastolic BP': int(data['diastolic_bp']),
            'Sleep Disorder': data.get('sleep_disorder', 'Nothing')
        }
        
        # Buat DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Feature engineering (sesuai training)
        input_df['BP_Ratio'] = input_df['Diastolic BP'] / input_df['Systolic BP']
        input_df['Age_Group'] = pd.cut(
            input_df['Age'], 
            bins=[18, 30, 45, 60, 100],
            labels=['Young', 'Adult', 'Mid-Age', 'Senior']
        )
        
        # Drop kolom yang tidak dipakai di model
        columns_to_drop = ['Sleep Disorder', 'Stress_Category']
        for col in columns_to_drop:
            if col in input_df.columns:
                input_df = input_df.drop(columns=[col])
        
        # Preprocess
        processed_data = preprocessor.transform(input_df)
        
        # Prediksi
        prediction = model.predict(processed_data)
        probability = model.predict_proba(processed_data)
        
        # Mapping stress level
        stress_mapping = {
            3: 'Low',
            4: 'Low', 
            5: 'Medium',
            6: 'Medium',
            7: 'High',
            8: 'High'
        }
        
        stress_level = stress_mapping.get(int(prediction[0]), 'Medium')
        
        return jsonify({
            'success': True,
            'stress_level': stress_level,
            'stress_score': int(prediction[0]),
            'confidence': float(max(probability[0])) * 100
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🤖 ML SERVER - LAPTOP 1")
    print("="*50)
    print("Server will run on: http://0.0.0.0:5001")
    print("\nMake sure these files exist:")
    print("  ✓ stress_predictor.pkl")
    print("  ✓ preprocessor.pkl")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)