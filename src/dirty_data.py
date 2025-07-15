import pandas as pd
import numpy as np

# Load original clean data
df = pd.read_csv("data/user_sessions.csv", parse_dates=["login_time"])
# 1. Add random NaNs
def add_nans(df, nan_ratio=0.03, exclude_cols=None):
    df = df.copy()
    exclude_cols = exclude_cols or []
    for col in df.columns:
        if col not in exclude_cols:
            mask = np.random.rand(len(df)) < nan_ratio
            df.loc[mask, col] = np.nan
    return df

df = add_nans(df, nan_ratio=0.03, exclude_cols=["user_id", "is_fake"])


# 2. Add random duplicates
def add_duplicates(df, ratio=0.05):
    n_duplicates = int(len(df) * ratio)
    duplicates = df.sample(n_duplicates, replace=True, random_state=42)
    return pd.concat([df, duplicates], ignore_index=True)

df = add_duplicates(df, ratio=0.05)

# 3. Add outliers to session_duration
def add_outliers(df, col="session_duration", ratio=0.01):
    df = df.copy()
    n_outliers = int(len(df) * ratio)
    std_dev = df[col].std()
    mean = df[col].mean()
    outlier_values = mean + 10 * std_dev * np.random.choice([-1, 1], size=n_outliers)
    indices = np.random.choice(df.index, size=n_outliers, replace=False)
    df.loc[indices, col] = outlier_values
    return df

df = add_outliers(df, col="session_duration", ratio=0.01)

# Save dirty dataset
df.to_csv("data/user_sessions_dirty.csv", index=False)
print("Dirty dataset saved to user_sessions_dirty.csv with shape:", df.shape)
