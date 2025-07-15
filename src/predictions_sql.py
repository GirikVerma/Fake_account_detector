import mysql.connector
import pandas as pd

# Load prediction output
df = pd.read_csv("Data/predictions.csv")

# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Giratina_615",
    database="fake_account_detection"
)
cursor = conn.cursor()

# Create the new table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        num_logins INT,
        avg_session_duration FLOAT,
        std_session_duration FLOAT,
        unique_ips INT,
        unique_devices INT,
        night_logins INT,
        active_days INT,
        logins_per_day FLOAT,
        user_id VARCHAR(255),
        is_fake BOOLEAN,
        anomaly_score FLOAT,
        is_flagged BOOLEAN
    )
""")

# Insert predictions
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO predictions (
            num_logins, avg_session_duration, std_session_duration, unique_ips,
            unique_devices, night_logins, active_days, logins_per_day,
            user_id, is_fake, anomaly_score, is_flagged
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
conn.close()
print("Predictions inserted into MySQL.")
