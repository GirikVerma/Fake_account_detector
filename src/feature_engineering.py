import pandas as pd

# Load the cleaned session data
df = pd.read_csv("data/user_sessions_clean.csv", parse_dates=["login_time"])

# 1. Extract additional time features

df['hour'] = df['login_time'].dt.hour
df['date'] = df['login_time'].dt.date


# 2. Group by user_id to engineer features

features = df.groupby('user_id').agg(
    num_logins=('session_duration', 'count'),
    avg_session_duration=('session_duration', 'mean'),
    std_session_duration=('session_duration', 'std'),
    unique_ips=('ip_address', pd.Series.nunique),
    unique_devices=('device', pd.Series.nunique),
    night_logins=('hour', lambda x: ((x >= 0) & (x < 5)).sum()),
    active_days=('date', pd.Series.nunique)
)


# 3. Derived metric: logins per active day

features['logins_per_day'] = features['num_logins'] / features['active_days']


# 4. Add is_fake label

user_labels = df[['user_id', 'is_fake']].drop_duplicates('user_id')
features = features.merge(user_labels, left_index=True, right_on='user_id')

# 5. Save features

features.to_csv("data/features.csv", index=False)
print(" Feature set saved to data/features.csv with shape:", features.shape)
