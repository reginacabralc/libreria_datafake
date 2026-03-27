import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_sales(n=500, seed=42, start_date="2024-01-01", end_date="2024-12-31"):
    np.random.seed(seed)
    Faker.seed(seed)

    categories = ["Electronics", "Clothing", "Food", "Home", "Sports", "Beauty"]
    payment_methods = ["card", "transfer", "cash", "paypal"]
    statuses = ["completed", "returned", "pending"]

    customer_ids = [f"CUST_{str(i).zfill(4)}" for i in range(1, 201)]
    product_ids = [f"PROD_{str(i).zfill(4)}" for i in range(1, 51)]

    dates = pd.date_range(start=start_date, end=end_date, periods=n)

    df = pd.DataFrame({
        "sale_id": [f"SALE_{str(i).zfill(6)}" for i in range(1, n + 1)],
        "date": np.random.choice(dates, size=n),
        "customer_id": np.random.choice(customer_ids, size=n),
        "product_id": np.random.choice(product_ids, size=n),
        "category": np.random.choice(categories, size=n, p=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05]),
        "quantity": np.random.randint(1, 10, size=n),
        "unit_price": np.round(np.random.lognormal(mean=4.5, sigma=1.0, size=n), 2),
        "payment_method": np.random.choice(payment_methods, size=n, p=[0.55, 0.25, 0.12, 0.08]),
        "status": np.random.choice(statuses, size=n, p=[0.88, 0.07, 0.05]),
        "store": [fake.city() for _ in range(n)],
    })

    df["revenue"] = np.round(df["quantity"] * df["unit_price"], 2)
    df["date"] = pd.to_datetime(df["date"]).dt.date

    return df.sort_values("date").reset_index(drop=True)