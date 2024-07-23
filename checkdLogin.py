import mysql.connector
from mysql.connector import Error


def check_login(user_id, user_password):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='mozzy_guard_db',
            user='root',
            password='0000'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT user_password FROM user WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result is None:
                return {"success": False, "message": "존재하지 않는 회원입니다."}
            else:
                stored_password = result['user_password']
                if user_password == stored_password:
                    return {"success": True, "message": "로그인 성공!"}
                else:
                    return {"success": False, "message": "비밀번호가 틀렸습니다."}

    except Error as e:
        return {"success": False, "message": f"Error: {e}"}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
