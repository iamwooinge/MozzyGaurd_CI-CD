import mysql.connector
from mysql_config import mysql_db

# 데이터베이스 연결
conn = mysql.connector.connect(
    host=mysql_db['host'],
    port=mysql_db['port'],
    database=mysql_db['database'],
    user=mysql_db['user'],
    password=mysql_db['password']
)

cursor = conn.cursor()

# user 테이블 생성 - 필요한 경우만 실행
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    user_id VARCHAR(255) PRIMARY KEY,
    user_password VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL
)
''')

conn.commit()

def create_user(user_id, password, email):
    # 중복 ID 확인
    cursor.execute('SELECT user_id FROM user WHERE user_id = %s', (user_id,))
    if cursor.fetchone() is not None:
        return "이미 존재하는 회원입니다."
    
    # 데이터 삽입
    cursor.execute('INSERT INTO user (user_id, user_password, user_email) VALUES (%s, %s, %s)', (user_id, password, email))
    conn.commit()
    return "회원가입 성공"

def main():
    user_id = input("Enter ID: ")
    user_password = input("Enter Password: ")
    user_email = input("Enter Email: ")
    
    result = create_user(user_id, user_password, user_email)
    print(result)

if __name__ == '__main__':
    main()
