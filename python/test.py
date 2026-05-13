import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="fakenewsdetectiondb"
    )
    print("Connected successfully")
except Exception as e:
    print("Error:", e)