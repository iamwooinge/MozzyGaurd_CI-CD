import math
from getCoord import latlng

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

def getXY():
    map = LamcParameter()
    lat = latlng[0]
    lon = latlng[1]
    x, y = lamcproj(lon, lat, map)
    x = math.floor(x + 0.5)+1
    y = math.floor(y + 0.5)+1
    print(f"lon.= {lon}, lat.= {lat} ---> X = {x}, Y = {y}")
    
    grid = [x, y]
    # print(grid)
    return grid

# 위도, 경도를 이용해 x, y 좌표 반환 grid = [x, y]