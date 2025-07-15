import mysql.connector
import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Giratina_615",
    database="fake_account_detection"
)
cursor = conn.cursor()

# Load CSV
df = pd.read_csv('Data/user_sessions_clean.csv')

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_sessions (
    user_id VARCHAR(255),
    is_fake INT,
    login_time DATETIME,
    session_duration FLOAT,
    ip_address VARCHAR(255),
    device VARCHAR(255)
)
""")
cursor.execute("TRUNCATE TABLE user_sessions")
# Insert data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO user_sessions (user_id, is_fake, login_time, session_duration, ip_address, device)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['user_id'],
        int(row['is_fake']),
        row['login_time'],
        float(row['session_duration']),
        row['ip_address'],
        row['device']
    ))

conn.commit()
cursor.close()
conn.close()

print("Data inserted into user_sessions table.")

