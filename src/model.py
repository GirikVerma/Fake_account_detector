import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

# Load engineered features
df = pd.read_csv("data/features.csv")


# 1. Prepare data for model

X = df.drop(columns=["user_id", "is_fake"])  # unsupervised
user_ids = df["user_id"]


# 2. Train Isolation Forest

model = IsolationForest(n_estimators=100, contamination=0.2, random_state=42)
df['anomaly_score'] = model.fit_predict(X)
df['anomaly_score'] = model.decision_function(X)
df['is_flagged'] = model.predict(X)  # -1 = anomaly, 1 = normal
df['is_flagged'] = df['is_flagged'].apply(lambda x: 1 if x == -1 else 0)


# 3. Save predictions

df['user_id'] = user_ids
df.to_csv("data/predictions.csv", index=False)
print("Model predictions saved to data/predictions.csv with shape:", df.shape)

# Optional: basic stats
flagged = df['is_flagged'].sum()
print(f" Users flagged as anomalies: {flagged} out of {len(df)}")
