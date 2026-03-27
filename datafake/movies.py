import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_movies(n=500, seed=42):
    """
    Generate a synthetic movies/streaming dataset.

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

    genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Documentary", "Animation"]
    platforms = ["Netflix", "HBO Max", "Disney+", "Amazon Prime", "Apple TV+"]
    ratings = ["G", "PG", "PG-13", "R", "NC-17"]
    languages = ["English", "Spanish", "French", "Japanese", "Korean", "Italian"]

    df = pd.DataFrame({
        "movie_id": [f"MOV_{str(i).zfill(5)}" for i in range(1, n + 1)],
        "title": [fake.catch_phrase() for _ in range(n)],
        "genre": np.random.choice(genres, size=n, p=[0.20, 0.15, 0.20, 0.10, 0.12, 0.10, 0.08, 0.05]),
        "platform": np.random.choice(platforms, size=n, p=[0.35, 0.20, 0.20, 0.15, 0.10]),
        "release_year": np.random.randint(1970, 2025, size=n),
        "duration_min": np.random.randint(75, 210, size=n),
        "rating": np.random.choice(ratings, size=n, p=[0.05, 0.15, 0.40, 0.35, 0.05]),
        "language": np.random.choice(languages, size=n, p=[0.50, 0.20, 0.10, 0.08, 0.07, 0.05]),
        "imdb_score": np.round(np.random.normal(loc=6.5, scale=1.2, size=n).clip(1, 10), 1),
        "votes": np.random.lognormal(mean=10, sigma=2, size=n).astype(int),
        "box_office_usd": np.random.lognormal(mean=17, sigma=2, size=n).astype(int),
        "sequel": np.random.choice([True, False], size=n, p=[0.20, 0.80]),
    })

    return df.reset_index(drop=True)