from flask import Flask, jsonify, render_template, request, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import geocoder
from geopy.geocoders import Nominatim
import joblib
import pandas as pd
from createUser import create_user
import checkdLogin
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key') 

CORS(app)

# 모델 및 스케일러 로드
model = joblib.load('models/best_rf_model.pkl')
scaler = joblib.load('models/scaler.pkl')

# 로그인 상태 확인
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))  # 로그인 페이지로 리디렉션
        return f(*args, **kwargs)
    return decorated_function

# Get the current location based on IP address
g = geocoder.ip('me')

# 위도, 경도 추출
latlng = g.latlng

# 현재 위치 위도, 경도 출력
print(f"Latitude: {latlng[0]}, Longitude: {latlng[1]}")

def geocoding_reverse(lat, lng):
    geolocoder = Nominatim(user_agent='South Korea', timeout=None)
    location = geolocoder.reverse((lat, lng))

    if location:
        address = location.address
        address_parts = address.split(', ')
        
        # 시와 구를 저장할 변수
        city = None
        district = None
        
        # "시"와 "구"를 포함한 부분을 찾기
        for part in address_parts:
            if part.endswith("시"):
                city = part
            elif part.endswith("구"):
                district = part
                
        return city, district
    else:
        return None, None

def predict_mosquito_risk(temp_high, temp_low, rainfall, humidity):
    input_data = pd.DataFrame([[temp_high, temp_low, rainfall, humidity]], columns=['최고기온', '최저기온', '강수량(mm)', '평균습도'])
    input_scaled = scaler.transform(input_data)
    risk_index = model.predict(input_scaled)
    return risk_index[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup_route():
    data = request.get_json()
    user_id = data.get('userId')
    user_password = data.get('password')
    user_email = data.get('email')

    if not user_id or not user_password or not user_email:
        return jsonify({'message': 'Invalid input'}), 400
    
    result = create_user(user_id, user_password, user_email)
    return jsonify({'message': result})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('username')
    user_password = data.get('password')
    result = checkdLogin.check_login(user_id, user_password)

    if result.get('success'):  # 로그인 성공
        session['user_id'] = user_id
        return jsonify({'message': 'Login successful', 'success': True})
    else:
        return jsonify({'message': 'Login failed', 'success': False})

@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('user_id', None)
    # Redirect to the root index.html
    return redirect(url_for('index'))

@app.route('/map')
@login_required # 로그인 상태일 때만 접근 가능
def map():
    return render_template('map.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    temp_high = data['temp_high']
    temp_low = data['temp_low']
    rainfall = data['rainfall']
    humidity = data['humidity']
    
    # 모기 위험 지수 예측
    prediction = predict_mosquito_risk(temp_high, temp_low, rainfall, humidity)
    
    # 예측값에 따라 mosquito_index 값 설정
    if 0 <= prediction < 25:
        mosquito_index = 0
    elif 25 <= prediction < 50:
        mosquito_index = 1
    elif 50 <= prediction < 75:
        mosquito_index = 2
    else:  # prediction >= 75
        mosquito_index = 3
    
    # 예측값과 모기 지수를 응답으로 반환
    return jsonify({'mosquito_risk_index': prediction, 'mosquito_index': mosquito_index})


@app.route('/image', methods=['GET'])
def image():
    # 예제 모기 지수 값 (이 값은 실제 API 호출로 대체됨)
    mosquito_index = request.args.get('mosquito_index', type=int)
    
    # 이미지 URL을 반환
    image_urls = {
        0: 'static/img/mosquito_low.png',
        1: 'static/img/mosquito_medium_low.png',
        2: 'static/img/mosquito_medium_high.png',
        3: 'static/img/mosquito_high.png'
    }
    
    # 기본 이미지
    image_url = image_urls.get(mosquito_index, 'static/img/mosquito_default.png')
    
    return jsonify({'image_url': image_url})

if __name__ == '__main__':
    app.run(debug=True, port=5500)
