import math
import requests
import datetime
import xml.etree.ElementTree as ET
from urllib.parse import urlencode, unquote

NX = 149  # X축 격자점 수
NY = 253  # Y축 격자점 수

class LamcParameter:
    def __init__(self):
        self.Re = 6371.00877  # 사용할 지구반경 [ km ]
        self.grid = 5.0  # 격자간격 [ km ]
        self.slat1 = 30.0  # 표준위도 [degree]
        self.slat2 = 60.0  # 표준위도 [degree]
        self.olon = 126.0  # 기준점의 경도 [degree]
        self.olat = 38.0  # 기준점의 위도 [degree]
        self.xo = 210 / self.grid  # 기준점의 X좌표 [격자거리]
        self.yo = 675 / self.grid  # 기준점의 Y좌표 [격자거리]
        self.first = 0  # 시작여부 (0 = 시작)

def lamcproj(lon, lat, map):
    PI = math.asin(1.0) * 2.0
    DEGRAD = PI / 180.0
    RADDEG = 180.0 / PI

    if map.first == 0:
        re = map.Re / map.grid
        slat1 = map.slat1 * DEGRAD
        slat2 = map.slat2 * DEGRAD
        olon = map.olon * DEGRAD
        olat = map.olat * DEGRAD

        sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
        sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
        sf = math.tan(PI * 0.25 + slat1 * 0.5)
        sf = (sf ** sn) * math.cos(slat1) / sn
        ro = math.tan(PI * 0.25 + olat * 0.5)
        ro = re * sf / (ro ** sn)
        map.re, map.slat1, map.slat2, map.olon, map.olat, map.sn, map.sf, map.ro = re, slat1, slat2, olon, olat, sn, sf, ro
        map.first = 1

    ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
    ra = map.re * map.sf / (ra ** map.sn)
    theta = lon * DEGRAD - map.olon
    if theta > PI:
        theta -= 2.0 * PI
    if theta < -PI:
        theta += 2.0 * PI
    theta *= map.sn
    x = ra * math.sin(theta) + map.xo
    y = map.ro - ra * math.cos(theta) + map.yo

    return x, y

def getXY(latitude, longitude):
    map = LamcParameter()
    lat = latitude
    lon = longitude
    x, y = lamcproj(lon, lat, map)
    x = math.floor(x + 0.5)+1
    y = math.floor(y + 0.5)+1
    print(f"lon.= {lon}, lat.= {lat} ---> X = {x}, Y = {y}")
    
    grid = [x, y]
    # print(grid)
    return grid

def getWeather(nx, ny):
    # 공공데이터포털 API 키
    key = "LtdxOHrcMwiMD%2BePsgB0et3yhiPhClBBWX5o5IBrjsyJv95ixqjCjuHIRvX2KqKpZ3J6Zrk39xxAk8N9aSeu%2BQ%3D%3D"
    api_key = unquote(unquote(key))

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

    return result