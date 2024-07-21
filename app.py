from flask import Flask, jsonify, render_template
from geopy.geocoders import Nominatim
import requests
import geocoder

app = Flask(__name__)

# Get the current location based on IP address
g = geocoder.ip('me')
# print(g)

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

@app.route('/')
def index():
    lat = latlng[0]
    lng = latlng[1]
    city, district = geocoding_reverse(lat, lng)
    return render_template('index.html', city=city, district=district)

if __name__ == '__main__':
    app.run(debug=True)
