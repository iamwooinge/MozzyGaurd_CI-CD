# mysql_config.py
import pymysql.cursors
import mysql.connector
from mysql.connector import Error

mysql_db = {
    "user": "root",
    "password": "1234",
    "host": "10.13.48.3",
    "port": 3306,
    "database": "mozzy_guard_db",
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=mysql_db['host'],
            port=mysql_db['port'],
            database=mysql_db['database'],
            user=mysql_db['user'],
            password=mysql_db['password']
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
    
