import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_users(n=300, seed=42):
    np.random.seed(seed)
    Faker.seed(seed)

    plans = ["free", "basic", "pro", "enterprise"]
    devices = ["mobile", "desktop", "tablet"]
    statuses = ["active", "inactive", "churned"]

    df = pd.DataFrame({
        "user_id": [f"USR_{str(i).zfill(5)}" for i in range(1, n + 1)],
        "name": [fake.name() for _ in range(n)],
        "email": [fake.email() for _ in range(n)],
        "country": [fake.country() for _ in range(n)],
        "age": np.random.randint(18, 65, size=n),
        "plan": np.random.choice(plans, size=n, p=[0.55, 0.25, 0.15, 0.05]),
        "device": np.random.choice(devices, size=n, p=[0.55, 0.35, 0.10]),
        "sessions_per_month": np.random.poisson(lam=12, size=n),
        "avg_session_minutes": np.round(np.random.lognormal(mean=2.5, sigma=0.8, size=n), 1),
        "status": np.random.choice(statuses, size=n, p=[0.70, 0.20, 0.10]),
        "registration_date": [fake.date_between(start_date="-3y", end_date="today") for _ in range(n)],
    })

    df["churned"] = (df["status"] == "churned").astype(int)

    return df.reset_index(drop=True)