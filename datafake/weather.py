import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_weather(n=500, seed=42, start_date="2024-01-01", end_date="2024-12-31"):
    """
    Generate a synthetic weather dataset.

    Parameters
    ----------
    n : int
        Number of rows to generate.
    seed : int
        Random seed for reproducibility.
    start_date : str
        Start date (YYYY-MM-DD).
    end_date : str
        End date (YYYY-MM-DD).

    Returns
    -------
    pd.DataFrame
    """
    np.random.seed(seed)
    Faker.seed(seed)

    cities = [
        "Mexico City", "New York", "London", "Tokyo", "Paris",
        "Sydney", "Toronto", "Berlin", "Dubai", "São Paulo"
    ]
    conditions = ["Sunny", "Cloudy", "Rainy", "Stormy", "Snowy", "Windy", "Foggy"]

    dates = pd.date_range(start=start_date, end=end_date, periods=n)

    df = pd.DataFrame({
        "record_id": [f"WTH_{str(i).zfill(6)}" for i in range(1, n + 1)],
        "date": np.random.choice(dates, size=n),
        "city": np.random.choice(cities, size=n),
        "temperature_c": np.round(np.random.normal(loc=18, scale=12, size=n), 1),
        "humidity_pct": np.round(np.random.uniform(20, 100, size=n), 1),
        "wind_speed_kmh": np.round(np.random.lognormal(mean=2.5, sigma=0.8, size=n), 1),
        "precipitation_mm": np.round(np.random.exponential(scale=5, size=n), 1),
        "condition": np.random.choice(conditions, size=n, p=[0.30, 0.25, 0.20, 0.08, 0.07, 0.06, 0.04]),
        "uv_index": np.random.randint(0, 11, size=n),
        "visibility_km": np.round(np.random.uniform(1, 30, size=n), 1),
    })

    df["date"] = pd.to_datetime(df["date"]).dt.date

    return df.sort_values("date").reset_index(drop=True)