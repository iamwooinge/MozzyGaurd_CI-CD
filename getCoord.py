import geocoder

# Get the current location based on IP address
g = geocoder.ip('me')
# print(g)

# 위도, 경도 추출
latlng = g.latlng

# 현재 위치 위도, 경도 출력
print(f"Latitude: {latlng[0]}, Longitude: {latlng[1]}")
