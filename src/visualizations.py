import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Giratina_615",
    database="fake_account_detection"
)

#Checking how many flags are correct, or incorrect
query = """
SELECT is_flagged, is_fake, COUNT(*) AS count
FROM predictions
GROUP BY is_flagged, is_fake;
"""
df_confusion = pd.read_sql(query, conn)

sns.barplot(data=df_confusion, x='is_flagged', y='count', hue='is_fake')
plt.title("Flagged vs. Actual Label Breakdown")
plt.xlabel("Flagged by Model (0 = No, 1 = Yes)")
plt.ylabel("Number of Users")
plt.legend(title="Actual Fake (1 = Fake, 0 = Real)")
plt.tight_layout()
plt.savefig("flagged_vs_actual.png")
plt.show()


#analyzing information about real users who were flagged
query = """
SELECT 
    ROUND(AVG(num_logins), 2) AS avg_logins,
    ROUND(AVG(avg_session_duration), 2) AS avg_duration,
    ROUND(AVG(night_logins), 2) AS avg_night_logins,
    ROUND(AVG(anomaly_score), 4) AS avg_anomaly_score
FROM predictions
WHERE is_fake = 0 AND is_flagged = 1;
"""
false_positives = pd.read_sql(query, conn).T.reset_index()
false_positives.columns = ['Feature', 'Value']

sns.barplot(data=false_positives, x='Value', y='Feature')
plt.title("Behavior of Real Users Who Were Falsely Flagged")
plt.xlabel("Average Value")
plt.ylabel("Feature")
plt.tight_layout()
plt.savefig("false_positives.png")
plt.show()


#Data about fake users who were not flagged
query = """
SELECT 
    ROUND(AVG(num_logins), 2) AS avg_logins,
    ROUND(AVG(avg_session_duration), 2) AS avg_duration,
    ROUND(AVG(night_logins), 2) AS avg_night_logins,
    ROUND(AVG(anomaly_score), 4) AS avg_anomaly_score
FROM predictions
WHERE is_fake = 1 AND is_flagged = 0;
"""
false_negatives = pd.read_sql(query, conn).T.reset_index()
false_negatives.columns = ['Feature', 'Value']

sns.barplot(data=false_negatives, x='Value', y='Feature')
plt.title("Behavior of Fake Users Who Were Missed by the Model")
plt.xlabel("Average Value")
plt.ylabel("Feature")
plt.tight_layout()
plt.savefig("false_negatives.png")
plt.show()
