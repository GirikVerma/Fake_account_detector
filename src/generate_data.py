import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_user_data(n_users=500, fake_ratio=0.2):
    data = []
    for i in range(n_users):
        is_fake = int(i < int(n_users * fake_ratio)) 
        user_id = f"user_{i+1}"
        creation_date = fake.date_between(start_date='-1y', end_date='-1d')
        num_sessions = random.randint(3, 15) if not is_fake else random.randint(20, 50)
        
        for _ in range(num_sessions):
            login_time = fake.date_time_between(start_date=creation_date, end_date='now')
            session_duration = random.uniform(300, 3600) if not is_fake else random.uniform(30, 300)  
            ip_address = fake.ipv4_public() if not is_fake else random.choice([
                fake.ipv4_public() for _ in range(3)
            ])
            device = random.choice(["Windows", "Android", "iOS", "MacOS"])
            
            data.append({
                "user_id": user_id,
                "is_fake": is_fake,
                "login_time": login_time,
                "session_duration": round(session_duration, 2),
                "ip_address": ip_address,
                "device": device
            })
    
    return pd.DataFrame(data)

df = generate_user_data()
df.to_csv("data/user_sessions.csv", index=False)
print("Dataset saved to user_sessions.csv")
