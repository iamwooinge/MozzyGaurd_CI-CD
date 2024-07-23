import requests
import datetime
import xml.etree.ElementTree as ET
from urllib.parse import urlencode, unquote
import coordConverter
from getCoord import latlng

# 공공데이터포털 API 키
key = "LtdxOHrcMwiMD%2BePsgB0et3yhiPhClBBWX5o5IBrjsyJv95ixqjCjuHIRvX2KqKpZ3J6Zrk39xxAk8N9aSeu%2BQ%3D%3D"
api_key = unquote(unquote(key))

# 현재 위치의 좌표 (위도, 경도)
latitude = latlng[1]
longitude = latlng[0]

# API 요청을 위한 기본 파라미터 설정
grid = coordConverter.getXY()
nx = grid[0]
ny = grid[1]

# 현재 시각을 기준으로 가장 가까운 3시간 간격의 base_time 설정
def get_nearest_base_time(current_time):
    hours = [2, 5, 7, 11, 14, 17, 20, 23]
    nearest_hour = min(hours, key=lambda h: abs(h - current_time.hour))
    return f"{nearest_hour:02d}00"

# 현재 시각 및 base_time 설정
def get_base_time():
    current_time = datetime.datetime.now()
    return get_nearest_base_time(current_time)

# base_time을 3시간 이전으로 조정
def adjust_base_time(base_time):
    base_hour = int(base_time[:2])
    adjusted_hour = base_hour - 3
    if adjusted_hour < 0:
        adjusted_hour += 24
    return f"{adjusted_hour:02d}00"

# Function to fetch weather data from the first API (getVilageFcst)
def fetch_vilage_fcst_data(base_date, base_time):
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        "serviceKey": api_key,  # 인코딩된 API 키 사용
        "pageNo": "1",
        "numOfRows": "1000",
        "dataType": "xml",  # XML 형식으로 요청
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny
    }
    full_url = f"{url}?{urlencode(params, safe=':=')}"
    print("Fetching URL:", full_url)
    response = requests.get(full_url)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)
            header = root.find('header')
            body = root.find('body')

            if header is None or body is None:
                print("Error: XML 구조가 예상과 다릅니다.")
                return None

            result_code = header.find('resultCode')
            result_msg = header.find('resultMsg')

            if result_code is None or result_msg is None:
                print("Error: resultCode 또는 resultMsg 요소가 누락되었습니다.")
                return None

            result_code = result_code.text
            result_msg = result_msg.text

            if result_code == '03':
                print(f"Error: {result_msg}")
                return None
            elif result_code == '04':
                print("No data available for the given date.")
                return None
            else:
                # XML에서 기온, 최저 기온, 최고 기온 추출
                min_temperature = None
                max_temperature = None

                items = body.find('items').findall('item')

                for item in items:
                    category = item.find('category').text
                    if category == 'TMN':
                        min_temperature = item.find('fcstValue').text
                    elif category == 'TMX':
                        max_temperature = item.find('fcstValue').text

                return {
                    "min_temperature": min_temperature,
                    "max_temperature": max_temperature
                }
        except ET.ParseError as e:
            print(f"Error: XML 응답을 처리하는 중 오류가 발생했습니다. {e}")
            return None
    else:
        print("Error: API 요청이 실패했습니다.")
        return None

# Function to fetch real-time weather data from the second API (getUltraSrtNcst)
def fetch_ultra_srt_ncst_data(base_date, base_time):
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    params = {
        "serviceKey": api_key,  # 인코딩된 API 키 사용
        "pageNo": "1",
        "numOfRows": "1000",
        "dataType": "xml",  # XML 형식으로 요청
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny
    }
    full_url = f"{url}?{urlencode(params, safe=':=')}"
    print("Fetching URL:", full_url)
    print(f"현재 base_time: {base_time}")
    response = requests.get(full_url)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)
            header = root.find('header')
            body = root.find('body')

            if header is None or body is None:
                print("Error: XML 구조가 예상과 다릅니다.")
                return None

            result_code = header.find('resultCode')
            result_msg = header.find('resultMsg')

            if result_code is None or result_msg is None:
                print("Error: resultCode 또는 resultMsg 요소가 누락되었습니다.")
                return None

            result_code = result_code.text
            result_msg = result_msg.text

            if result_code == '03':
                print(f"Error: {result_msg}")
                return None
            elif result_code == '04':
                print("No data available for the given date.")
                return None
            else:
                # XML에서 습도 및 강수량 추출
                humidity = None
                precipitation = None

                items = body.find('items').findall('item')

                for item in items:
                    category = item.find('category').text
                    if category == 'REH':
                        humidity = item.find('obsrValue').text
                    elif category == 'RN1':
                        precipitation = item.find('obsrValue').text

                return {
                    "humidity": humidity,
                    "precipitation": precipitation
                }
        except ET.ParseError as e:
            print(f"Error: XML 응답을 처리하는 중 오류가 발생했습니다. {e}")
            return None
    else:
        print("Error: API 요청이 실패했습니다.")
        return None

# 오늘 날짜와 base_time 설정
base_date = datetime.datetime.now().strftime("%Y%m%d")
base_time = get_base_time()

# 오늘 날짜로 데이터 요청
weather_data = fetch_vilage_fcst_data(base_date, base_time)
ultra_srt_ncst_data = fetch_ultra_srt_ncst_data(base_date, base_time)

# 데이터가 없을 경우, base_time을 3시간 이전으로 조정하고 재시도
if weather_data is None or ultra_srt_ncst_data is None:
    base_time = adjust_base_time(base_time)
    print(f"Retrying with adjusted base_time: {base_time}")
    weather_data = fetch_vilage_fcst_data(base_date, base_time)
    ultra_srt_ncst_data = fetch_ultra_srt_ncst_data(base_date, base_time)

# 데이터가 여전히 없을 경우, 자정부터 2시 사이일 경우에만 날짜를 전날로 변경하여 요청
if weather_data is None or ultra_srt_ncst_data is None:
    current_time = datetime.datetime.now()
    if current_time.hour < 2 or (current_time.hour == 2 and current_time.minute == 0):
        yesterday = current_time - datetime.timedelta(1)
        base_date = yesterday.strftime("%Y%m%d")
        base_time = "2300"  # 전날 데이터 요청 시 base_time을 2300으로 고정
        print(f"Fetching data for previous day: {base_date} with base_time {base_time}")
        weather_data = fetch_vilage_fcst_data(base_date, base_time)
        ultra_srt_ncst_data = fetch_ultra_srt_ncst_data(base_date, base_time)

# 결과 통합
result = {
    "humidity": ultra_srt_ncst_data.get('humidity') if ultra_srt_ncst_data else None,
    "min_temperature": weather_data.get('min_temperature') if weather_data else None,
    "max_temperature": weather_data.get('max_temperature') if weather_data else None,
    "precipitation": ultra_srt_ncst_data.get('precipitation') if ultra_srt_ncst_data else None
}

# 결과 출력
print(f"습도: {result.get('humidity')}%")
print(f"최저 기온: {result.get('min_temperature')}°C")
print(f"최고 기온: {result.get('max_temperature')}°C")
print(f"강수량: {result.get('precipitation')}mm")

# 현재 위치의 날씨 API 정보 출력
# 습도, 최저 기온, 최고 기온, 강수량
# NO_DATA 에러(현재 시간에서 데이터 찾을 수 없음) 발생 시 3시간 전에 발표된 데이터 자료 출력