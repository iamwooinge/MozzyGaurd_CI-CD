import mysql.connector
from getAddress import district

def get_location_coordinates(location_district):
    try:
        # MySQL 데이터베이스에 연결 (매개변수를 필요에 따라 조정하세요)
        conn = mysql.connector.connect(
            host='localhost',     # e.g., 'localhost' or '127.0.0.1'
            port=3306, 
            database='mozzy_guard_db', # e.g., 'test_db'
            user='root',     # e.g., 'root'
            password='mozzyguard',  # your password
            charset='utf-8'
        )
        cursor = conn.cursor()

        # SQL 쿼리 준비 및 실행
        query = "SELECT location_x, location_y FROM location WHERE location_district = %s"
        cursor.execute(query, (location_district,))
        # 결과 가져오기
        result = cursor.fetchone()

        # 결과가 None이 아닌지 확인
        if result:
            location_x, location_y = result
            return location_x, location_y
        else:
            return None, None

    except mysql.connector.Error as e:
        print(f"오류가 발생했습니다: {e}")
        return None, None

    finally:
        if conn:
            conn.close()

# 사용 예시
location_district = district  # 실제 구 이름으로 교체하세요
location_x, location_y = get_location_coordinates(location_district)
if location_x is not None and location_y is not None:
    print(f"{location_district}의 좌표는 (X: {location_x}, Y: {location_y}) 입니다.")
else:
    print(f"{location_district}에 대한 좌표를 찾을 수 없습니다.")


# mozzy_guard_db에 저장된 구와 구의 좌표 불러온다.
# 사용자가 구를 선택하였을 때 DB 정보 출력하는 코드