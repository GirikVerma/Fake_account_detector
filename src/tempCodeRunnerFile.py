import pandas as pd
import numpy as np

# Load the dirty dataset
df = pd.read_csv("data/user_sessions_dirty.csv", parse_dates=["login_time"])

# 1. Handle Missing Values
# Drop rows with missing critical fields
df = df.dropna(subset=["session_duration", "login_time", "ip_address", "device"])

#  fill remaining NaNs in numeric fields
if df['session_duration'].isnull().any():
    df['session_duration'] = df['session_duration'].fillna(df['session_duration'].median())

# 2. Remove Duplicate Rows

df = df.drop_duplicates()


# 3. Trim Outliers using IQR
def trim_iqr_outliers(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

df = trim_iqr_outliers(df, "session_duration")


# Save Cleaned Data
df.to_csv("data/user_sessions_clean.csv", index=False)
print("Cleaned dataset saved to user_sessions_clean.csv with shape:", df.shape)
