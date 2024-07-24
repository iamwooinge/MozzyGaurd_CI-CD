from flask import Flask, jsonify, render_template, request, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import geocoder
from geopy.geocoders import Nominatim
import joblib
import pandas as pd
from createUser import create_user
from mysql_config import get_db_connection
from mysql_config import mysql_db
import checkdLogin
from functools import wraps
from coordConverter import getXY, getWeather
import numpy as np

app = Flask(__name__)
app.secret_key = "mozzy_guard"
CORS(app)

# 모델 및 스케일러 로드
model = joblib.load('models/mosquito_model.pkl')

# 로그인 상태 확인
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))  # 로그인 페이지로 리디렉션
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    return render_template('userLogin.html')

@app.route('/signup_page')
def signup_page():
    return render_template('userRegister.html')

@app.route('/health')
def health_check():
    return 'OK', 200

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

    print(user_id,user_password)
    print(result)
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

# 위치 가져오기
@app.route('/receive_location', methods=['POST'])
def receive_location():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type, expected application/json'}), 415

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if latitude is None or longitude is None:
        return jsonify({'error': 'Missing latitude or longitude'}), 400
    
    # 위도와 경도를 사용하여 x, y 좌표 계산
    grid = getXY(latitude, longitude)
    weathers = getWeather(grid[0], grid[1])
    
    # 결과를 JSON 형식으로 반환
    return jsonify({
        'x': grid[0],
        'y': grid[1],
        'humidity': weathers.get('humidity'),
        'min_temperature': weathers.get('min_temperature'),
        'max_temperature': weathers.get('max_temperature'),
        'precipitation': weathers.get('precipitation')
    })


@app.route('/map')
@login_required  # 로그인 상태일 때만 접근 가능
def map():
    return render_template('map.html')

def categorize_mosquito_risk(risk_index):
    if risk_index < 25:
        return 0
    elif 25 <= risk_index < 50:
        return 1
    elif 50 <= risk_index < 75:
        return 2
    else:
        return 3

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    print('Received data:', data)  # 디버깅을 위해 데이터 출력

    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    max_temp = data.get('max_temp')
    min_temp = data.get('min_temp')
    rainfall = data.get('rainfall')
    humidity = data.get('humidity')

    # 모든 값이 존재하는지 확인
    if year is None or month is None or day is None or \
       max_temp is None or min_temp is None or \
       rainfall is None or humidity is None:
        return jsonify({'error': 'Missing data'}), 400

    try:
        # 문자열을 float로 변환
        max_temp = float(max_temp)
        min_temp = float(min_temp)
        rainfall = float(rainfall)
        humidity = float(humidity)
    except ValueError:
        return jsonify({'error': 'Invalid number format'}), 400

    # 입력 데이터를 모델에 맞게 변환
    input_features = np.array([[year, month, day, max_temp, min_temp, rainfall, humidity]])
    
    # 예측 수행
    mosquito_risk_index = model.predict(input_features)[0]
    mosquito_index = categorize_mosquito_risk(mosquito_risk_index)

    print('Prediction result:', {
        'mosquito_risk_index': mosquito_risk_index,
        'mosquito_index': mosquito_index
    })

    return jsonify({
        'mosquito_risk_index': mosquito_risk_index,
        'mosquito_index': mosquito_index
    })



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

@app.route('/subscribe', methods=['POST'])
def subscribe():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '로그인이 필요합니다.'}), 401

    user_id = session['user_id']

    try:
        connection = get_db_connection()
        if connection is None:
            raise Exception('Database connection failed')
        
        cursor = connection.cursor()
        query = "UPDATE user SET user_subscribe = %s WHERE user_id = %s"
        cursor.execute(query, ('Y', user_id))
        connection.commit()

        return jsonify({'success': True, 'message': '구독 신청 완료!'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 구독 상태 확인 엔드포인트
@app.route('/subscribe/status', methods=['GET'])
def subscribe_status():
    if 'user_id' in session:
        user_id = session['user_id']
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = "SELECT user_subscribe FROM user WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                return jsonify({'success': True, 'subscribed': result[0] == 'Y'})
            else:
                return jsonify({'success': False, 'message': 'User not found'})
        except Error as e:
            return jsonify({'success': False, 'message': str(e)})
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return jsonify({'success': False, 'message': 'User not logged in'})

# 구독 상태 토글 엔드포인트
@app.route('/subscribe/toggle', methods=['POST'])
def subscribe_toggle():
    if 'user_id' in session:
        user_id = session['user_id']
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = "SELECT user_subscribe FROM user WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                new_status = 'N' if result[0] == 'Y' else 'Y'
                update_query = "UPDATE user SET user_subscribe = %s WHERE user_id = %s"
                cursor.execute(update_query, (new_status, user_id))
                connection.commit()
                return jsonify({'success': True, 'subscribed': new_status == 'Y'})
            else:
                return jsonify({'success': False, 'message': 'User not found'})
        except Error as e:
            return jsonify({'success': False, 'message': str(e)})
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return jsonify({'success': False, 'message': 'User not logged in'})


if __name__ == '__main__':
    app.run(debug=True, port=5500)
