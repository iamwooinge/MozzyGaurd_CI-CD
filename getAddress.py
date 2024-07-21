from geopy.geocoders import Nominatim
from getCoord import latlng

def geocoding_reverse(lat_lng_str): 
    geolocoder = Nominatim(user_agent='South Korea', timeout=None)
    location = geolocoder.reverse(lat_lng_str)

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

city, district = geocoding_reverse(f"{latlng[0]}, {latlng[1]}")

print(f"시: {city}, 구: {district}")