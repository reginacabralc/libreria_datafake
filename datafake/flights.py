import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_flights(n=500, seed=42):
    """
    Generate a synthetic flights dataset.

    Parameters
    ----------
    n : int
        Number of rows to generate.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
    """
    np.random.seed(seed)
    Faker.seed(seed)

    airlines = ["Delta", "United", "American", "Lufthansa", "Emirates",
                "Ryanair", "Air France", "British Airways", "Aeromexico", "LATAM"]
    airports = ["JFK", "LAX", "LHR", "CDG", "DXB", "NRT", "MEX", "GRU", "SYD", "FRA"]
    statuses = ["on_time", "delayed", "cancelled", "diverted"]
    classes = ["economy", "business", "first"]

    origins = np.random.choice(airports, size=n)
    destinations = np.array([np.random.choice([a for a in airports if a != o]) for o in origins])

    df = pd.DataFrame({
        "flight_id": [f"FLT_{str(i).zfill(6)}" for i in range(1, n + 1)],
        "date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(n)],
        "airline": np.random.choice(airlines, size=n),
        "origin": origins,
        "destination": destinations,
        "class": np.random.choice(classes, size=n, p=[0.75, 0.20, 0.05]),
        "duration_min": np.random.randint(60, 900, size=n),
        "distance_km": np.random.randint(200, 15000, size=n),
        "price_usd": np.round(np.random.lognormal(mean=5.5, sigma=1.0, size=n), 2),
        "status": np.random.choice(statuses, size=n, p=[0.70, 0.22, 0.05, 0.03]),
        "delay_min": np.where(
            np.random.choice(statuses, size=n, p=[0.70, 0.22, 0.05, 0.03]) == "delayed",
            np.random.randint(15, 300, size=n),
            0
        ),
        "passengers": np.random.randint(50, 400, size=n),
        "satisfaction": np.round(np.random.uniform(1, 10, size=n), 1),
    })

    return df.reset_index(drop=True)