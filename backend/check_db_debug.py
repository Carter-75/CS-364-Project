import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")

try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    dbs = [x[0] for x in cursor.fetchall()]
    print(f"Available Databases: {dbs}")
    
    target_db = os.getenv('DB_NAME')
    if target_db in dbs:
        print(f"SUCCESS: Database '{target_db}' exists.")
    else:
        print(f"FAILURE: Database '{target_db}' does NOT exist.")
        
except Exception as e:
    print(f"CONNECTION ERROR: {e}")
